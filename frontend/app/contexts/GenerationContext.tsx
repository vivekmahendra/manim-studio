import * as React from 'react';
import { api, APIError, type GenerateResponse } from '~/services/api';

// Generation states
export type GenerationStatus = 
  | 'idle'
  | 'analyzing'
  | 'generating'
  | 'rendering'
  | 'completed' 
  | 'failed'
  | 'error';

export interface GenerationState {
  status: GenerationStatus;
  prompt: string;
  result?: GenerateResponse;
  error?: string;
  startTime?: Date;
  completedTime?: Date;
  jobId?: string;
  progress: number;
  currentStep: string;
  estimatedTimeRemaining?: number;
}

export interface GenerationContextType {
  state: GenerationState;
  generateAnimation: (prompt: string, quality?: string) => Promise<void>;
  reset: () => void;
  clearError: () => void;
  isGenerating: () => boolean;
}

const GenerationContext = React.createContext<GenerationContextType | undefined>(undefined);

// Initial state
const initialState: GenerationState = {
  status: 'idle',
  prompt: '',
  progress: 0,
  currentStep: 'Ready to generate',
};

// State reducer
type GenerationAction = 
  | { type: 'START_GENERATION'; prompt: string; jobId: string }
  | { type: 'UPDATE_PROGRESS'; progress: number; currentStep: string; status: GenerationStatus }
  | { type: 'GENERATION_SUCCESS'; result: GenerateResponse }
  | { type: 'GENERATION_ERROR'; error: string }
  | { type: 'RESET' }
  | { type: 'CLEAR_ERROR' };

function generationReducer(state: GenerationState, action: GenerationAction): GenerationState {
  switch (action.type) {
    case 'START_GENERATION':
      return {
        ...state,
        status: 'analyzing',
        prompt: action.prompt,
        jobId: action.jobId,
        error: undefined,
        progress: 0,
        currentStep: 'Starting generation...',
        startTime: new Date(),
        completedTime: undefined,
      };
    
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        status: action.status,
        progress: action.progress,
        currentStep: action.currentStep,
      };
    
    case 'GENERATION_SUCCESS':
      return {
        ...state,
        status: 'completed',
        result: action.result,
        progress: 100,
        currentStep: 'Complete!',
        completedTime: new Date(),
        error: undefined,
      };
    
    case 'GENERATION_ERROR':
      return {
        ...state,
        status: 'error',
        error: action.error,
        currentStep: 'Generation failed',
        completedTime: new Date(),
      };
    
    case 'RESET':
      return {
        ...initialState,
      };
    
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: undefined,
      };
    
    default:
      return state;
  }
}

export function GenerationProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = React.useReducer(generationReducer, initialState);
  const pollIntervalRef = React.useRef<NodeJS.Timeout>();
  const pollErrorCountRef = React.useRef<number>(0);

  const pollJobStatus = React.useCallback(async (jobId: string) => {
    try {
      console.log('🔍 Polling job status:', jobId);
      const status = await api.getJobStatus(jobId);
      console.log('📋 Job status response:', jobId, status.status, status.progress);
      
      // Reset error count on successful poll
      pollErrorCountRef.current = 0;
      
      if (status.status === 'completed') {
        // Job completed successfully
        console.log('✅ Job completed successfully:', jobId);
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = undefined;
        }
        
        dispatch({
          type: 'GENERATION_SUCCESS',
          result: {
            video_url: status.video_url || '',
            code: status.code || '',
            scene_name: status.scene_name || '',
            status: 'success',
            description: 'Animation generated successfully',
            job_id: jobId,
            progress: 100,
            current_step: 'Complete!',
            method: status.method,
            model: status.model,
            sample_used: status.sample_used
          }
        });
      } else if (status.status === 'failed') {
        // Job failed
        console.log('❌ Job failed:', jobId, status.error);
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = undefined;
        }
        
        dispatch({
          type: 'GENERATION_ERROR',
          error: status.error || 'Generation failed'
        });
      } else {
        // Job still in progress
        const mappedStatus: GenerationStatus = 
          status.status === 'analyzing' ? 'analyzing' :
          status.status === 'generating' ? 'generating' :
          status.status === 'rendering' ? 'rendering' : 'generating';
          
        dispatch({
          type: 'UPDATE_PROGRESS',
          progress: status.progress,
          currentStep: status.current_step,
          status: mappedStatus
        });
      }
    } catch (error) {
      console.error('Error polling job status:', error);
      
      // Increment error count
      pollErrorCountRef.current += 1;
      
      // Allow up to 3 consecutive polling errors before giving up
      if (pollErrorCountRef.current < 3) {
        console.log(`⚠️ Polling error ${pollErrorCountRef.current}/3, will retry...`);
        // Don't stop polling - let it retry on next interval
        return;
      }
      
      // Too many consecutive errors - stop polling and show error
      console.error('❌ Too many polling errors, stopping job monitoring');
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = undefined;
      }
      
      dispatch({
        type: 'GENERATION_ERROR',
        error: error instanceof Error ? error.message : 'Failed to check generation status'
      });
    }
  }, []);

  const generateAnimation = React.useCallback(async (prompt: string, quality: string = 'medium') => {
    // Prevent double submission - only allow if idle or if previous generation failed/completed
    if (state.status !== 'idle' && state.status !== 'completed' && state.status !== 'error' && state.status !== 'failed') {
      console.log('Generation already in progress, ignoring request');
      return;
    }

    try {
      console.log('🚀 Starting new generation:', prompt);
      
      // Clear any existing polling interval first
      if (pollIntervalRef.current) {
        console.log('⏹️ Stopping old polling interval');
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = undefined;
      }
      
      // Reset polling error count for new generation
      pollErrorCountRef.current = 0;

      // Clean up previous job if exists - WAIT for it to complete
      if (state.jobId) {
        console.log('🧹 Cleaning up previous job:', state.jobId);
        try {
          await api.cleanupJob(state.jobId);
          console.log('✅ Previous job cleaned up successfully');
        } catch (error) {
          console.error('❌ Failed to cleanup previous job:', error);
          // Continue anyway - don't let cleanup failure block new generation
        }
      }

      // Start generation
      console.log('📡 Calling API to generate...');
      const response = await api.generate({
        prompt,
        quality
      });

      if (response.job_id) {
        console.log('🎯 New job created:', response.job_id);
        
        // Start with job-based flow
        dispatch({
          type: 'START_GENERATION',
          prompt,
          jobId: response.job_id
        });

        // Start polling for progress
        console.log('📊 Starting polling for job:', response.job_id);
        pollIntervalRef.current = setInterval(() => {
          pollJobStatus(response.job_id!);
        }, 1000); // Poll every second

        // Initial poll
        setTimeout(() => pollJobStatus(response.job_id!), 500);
      } else {
        // Direct response (fallback)
        dispatch({
          type: 'GENERATION_SUCCESS',
          result: response
        });
      }
    } catch (error) {
      console.error('Generation error:', error);
      
      let errorMessage = 'Failed to generate animation';
      if (error instanceof APIError) {
        errorMessage = error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      dispatch({
        type: 'GENERATION_ERROR',
        error: errorMessage
      });
    }
  }, [pollJobStatus, state.status, state.jobId]);

  const reset = React.useCallback(() => {
    // Clear any polling interval
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }
    
    // Clean up job if exists
    if (state.jobId) {
      api.cleanupJob(state.jobId).catch(console.error);
    }
    
    dispatch({ type: 'RESET' });
  }, [state.jobId]);

  const clearError = React.useCallback(() => {
    dispatch({ type: 'CLEAR_ERROR' });
  }, []);

  const isGenerating = React.useCallback(() => {
    return state.status !== 'idle' && state.status !== 'completed' && state.status !== 'error' && state.status !== 'failed';
  }, [state.status]);

  // Cleanup on unmount
  React.useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  const contextValue: GenerationContextType = {
    state,
    generateAnimation,
    reset,
    clearError,
    isGenerating,
  };

  return (
    <GenerationContext.Provider value={contextValue}>
      {children}
    </GenerationContext.Provider>
  );
}

export function useGeneration() {
  const context = React.useContext(GenerationContext);
  if (context === undefined) {
    throw new Error('useGeneration must be used within a GenerationProvider');
  }
  return context;
}

// URL state synchronization hook
export function useGenerationURLState() {
  const { state, generateAnimation } = useGeneration();
  
  return {
    state,
    generateFromURL: (prompt: string) => {
      if (prompt && state.status === 'idle') {
        generateAnimation(prompt);
      }
    }
  };
}