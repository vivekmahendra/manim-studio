import * as React from 'react';
import { api, APIError, type GenerateResponse } from '~/services/api';

// Generation states
export type GenerationStatus = 
  | 'idle'
  | 'generating'
  | 'completed' 
  | 'error';

export interface GenerationState {
  status: GenerationStatus;
  prompt: string;
  result?: GenerateResponse;
  error?: string;
  startTime?: Date;
  completedTime?: Date;
}

export interface GenerationContextType {
  state: GenerationState;
  generateAnimation: (prompt: string, quality?: string) => Promise<void>;
  reset: () => void;
  clearError: () => void;
}

const GenerationContext = React.createContext<GenerationContextType | undefined>(undefined);

// Initial state
const initialState: GenerationState = {
  status: 'idle',
  prompt: '',
};

// State reducer
type GenerationAction = 
  | { type: 'START_GENERATION'; prompt: string }
  | { type: 'GENERATION_SUCCESS'; result: GenerateResponse }
  | { type: 'GENERATION_ERROR'; error: string }
  | { type: 'RESET' }
  | { type: 'CLEAR_ERROR' };

function generationReducer(state: GenerationState, action: GenerationAction): GenerationState {
  switch (action.type) {
    case 'START_GENERATION':
      return {
        ...state,
        status: 'generating',
        prompt: action.prompt,
        error: undefined,
        startTime: new Date(),
        completedTime: undefined,
      };
    
    case 'GENERATION_SUCCESS':
      return {
        ...state,
        status: 'completed',
        result: action.result,
        error: undefined,
        completedTime: new Date(),
      };
    
    case 'GENERATION_ERROR':
      return {
        ...state,
        status: 'error',
        error: action.error,
        completedTime: new Date(),
      };
    
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: undefined,
        status: state.result ? 'completed' : 'idle',
      };
    
    case 'RESET':
      return initialState;
    
    default:
      return state;
  }
}

// Provider component
interface GenerationProviderProps {
  children: React.ReactNode;
}

export function GenerationProvider({ children }: GenerationProviderProps) {
  const [state, dispatch] = React.useReducer(generationReducer, initialState);

  const generateAnimation = React.useCallback(async (prompt: string, quality = 'medium') => {
    if (!prompt.trim()) {
      dispatch({ type: 'GENERATION_ERROR', error: 'Please enter a prompt' });
      return;
    }

    dispatch({ type: 'START_GENERATION', prompt: prompt.trim() });

    try {
      const result = await api.generate({ prompt: prompt.trim(), quality });
      dispatch({ type: 'GENERATION_SUCCESS', result });
    } catch (error) {
      let errorMessage = 'Failed to generate animation';
      
      if (error instanceof APIError) {
        errorMessage = error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      dispatch({ type: 'GENERATION_ERROR', error: errorMessage });
    }
  }, []);

  const reset = React.useCallback(() => {
    dispatch({ type: 'RESET' });
  }, []);

  const clearError = React.useCallback(() => {
    dispatch({ type: 'CLEAR_ERROR' });
  }, []);

  const contextValue = React.useMemo(() => ({
    state,
    generateAnimation,
    reset,
    clearError,
  }), [state, generateAnimation, reset, clearError]);

  return (
    <GenerationContext.Provider value={contextValue}>
      {children}
    </GenerationContext.Provider>
  );
}

// Hook to use the generation context
export function useGeneration() {
  const context = React.useContext(GenerationContext);
  if (context === undefined) {
    throw new Error('useGeneration must be used within a GenerationProvider');
  }
  return context;
}

// Hook to get generation duration
export function useGenerationDuration(state: GenerationState): number | null {
  return React.useMemo(() => {
    if (!state.startTime) return null;
    
    const endTime = state.completedTime || new Date();
    return endTime.getTime() - state.startTime.getTime();
  }, [state.startTime, state.completedTime]);
}

// Hook for URL state synchronization
export function useGenerationURLState() {
  const { state, generateAnimation } = useGeneration();

  React.useEffect(() => {
    // Initialize from URL params on mount
    const searchParams = new URLSearchParams(window.location.search);
    const promptFromURL = searchParams.get('prompt');
    
    if (promptFromURL && state.status === 'idle') {
      generateAnimation(promptFromURL);
    }
  }, []);

  // Update URL when generation starts
  React.useEffect(() => {
    if (state.status === 'generating' && state.prompt) {
      const url = new URL(window.location.href);
      url.searchParams.set('prompt', state.prompt);
      window.history.replaceState({}, '', url.toString());
    }
  }, [state.status, state.prompt]);
}