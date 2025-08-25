import * as React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Circle, Loader2, AlertCircle, RefreshCw, Clock } from 'lucide-react';
import { clsx } from 'clsx';
import { Button } from './ui/Button';
import { useGeneration } from '~/contexts/GenerationContext';

interface ProgressStep {
  id: string;
  label: string;
  description: string;
  icon: React.ReactNode;
}

const GENERATION_STEPS: ProgressStep[] = [
  {
    id: 'analyzing',
    label: 'Analyzing Prompt',
    description: 'Understanding your mathematical concept and requirements',
    icon: <Circle className="h-5 w-5" />
  },
  {
    id: 'generating',
    label: 'Generating Code',
    description: 'Creating Manim animation script with AI',
    icon: <Circle className="h-5 w-5" />
  },
  {
    id: 'rendering',
    label: 'Rendering Video',
    description: 'Producing your high-quality animation',
    icon: <Circle className="h-5 w-5" />
  },
  {
    id: 'completed',
    label: 'Complete',
    description: 'Your animation is ready!',
    icon: <CheckCircle className="h-5 w-5" />
  }
];

interface GenerationProgressProps {
  onRetry?: () => void;
  className?: string;
}

export function GenerationProgress({ onRetry, className }: GenerationProgressProps) {
  const { state, clearError, isGenerating } = useGeneration();
  
  // Calculate elapsed time
  const [elapsedTime, setElapsedTime] = React.useState<string>('0s');
  
  React.useEffect(() => {
    if (!state.startTime) return;
    
    const updateElapsed = () => {
      const elapsed = Date.now() - state.startTime!.getTime();
      const seconds = Math.floor(elapsed / 1000);
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      
      if (minutes > 0) {
        setElapsedTime(`${minutes}m ${remainingSeconds}s`);
      } else {
        setElapsedTime(`${seconds}s`);
      }
    };
    
    updateElapsed();
    const interval = setInterval(updateElapsed, 1000);
    
    return () => clearInterval(interval);
  }, [state.startTime]);

  // Map status to current step
  const getCurrentStepIndex = (): number => {
    switch (state.status) {
      case 'analyzing': return 0;
      case 'generating': return 1;
      case 'rendering': return 2;
      case 'completed': return 3;
      case 'error':
      case 'failed': 
        // Return the step where error occurred based on progress
        if (state.progress <= 20) return 0;
        if (state.progress <= 60) return 1;
        return 2;
      default: return 0;
    }
  };

  const currentStepIndex = getCurrentStepIndex();

  const getStepStatus = (stepIndex: number) => {
    if (state.status === 'error' || state.status === 'failed') {
      if (stepIndex < currentStepIndex) return 'completed';
      if (stepIndex === currentStepIndex) return 'error';
      return 'pending';
    }
    
    if (state.status === 'completed') {
      return 'completed';
    }
    
    if (stepIndex < currentStepIndex) {
      return 'completed';
    } else if (stepIndex === currentStepIndex) {
      return 'active';
    }
    
    return 'pending';
  };

  return (
    <div className={clsx('w-full max-w-2xl mx-auto', className)}>
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {state.status === 'error' || state.status === 'failed' 
            ? 'Generation Failed' 
            : state.status === 'completed' 
            ? 'Animation Complete!' 
            : 'Generating Your Animation'}
        </h2>
        
        <p className="text-gray-600 dark:text-gray-400 mb-2">
          {state.prompt && `"${state.prompt}"`}
        </p>
        
        {/* Real-time status */}
        <div className="flex items-center justify-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center space-x-1">
            <Clock className="h-4 w-4" />
            <span>{elapsedTime}</span>
          </div>
          
          {state.progress > 0 && (
            <div className="flex items-center space-x-2">
              <span>{state.progress}%</span>
              <div className="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-blue-500 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${state.progress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>
          )}
        </div>
        
        {/* Current step description */}
        {state.currentStep && (
          <p className="text-sm text-blue-600 dark:text-blue-400 mt-2 font-medium">
            {state.currentStep}
          </p>
        )}
      </div>

      {/* Progress Steps */}
      <div className="space-y-4">
        {GENERATION_STEPS.map((step, index) => {
          const status = getStepStatus(index);
          
          return (
            <motion.div
              key={step.id}
              className={clsx(
                'flex items-start space-x-4 p-4 rounded-lg transition-all duration-300',
                status === 'active' && 'bg-blue-50 dark:bg-blue-900/20 ring-2 ring-blue-200 dark:ring-blue-800',
                status === 'completed' && 'bg-green-50 dark:bg-green-900/20',
                status === 'error' && 'bg-red-50 dark:bg-red-900/20 ring-2 ring-red-200 dark:ring-red-800'
              )}
              initial={{ opacity: 0.5 }}
              animate={{ 
                opacity: status === 'pending' ? 0.5 : 1,
                scale: status === 'active' ? 1.02 : 1
              }}
              transition={{ duration: 0.2 }}
            >
              {/* Icon */}
              <div className={clsx(
                'flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300',
                status === 'pending' && 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400',
                status === 'active' && 'bg-blue-100 dark:bg-blue-800 text-blue-600 dark:text-blue-400',
                status === 'completed' && 'bg-green-100 dark:bg-green-800 text-green-600 dark:text-green-400',
                status === 'error' && 'bg-red-100 dark:bg-red-800 text-red-600 dark:text-red-400'
              )}>
                {status === 'active' ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : status === 'completed' ? (
                  <CheckCircle className="h-5 w-5" />
                ) : status === 'error' ? (
                  <AlertCircle className="h-5 w-5" />
                ) : (
                  step.icon
                )}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <h3 className={clsx(
                  'text-sm font-medium transition-colors duration-300',
                  status === 'pending' && 'text-gray-500 dark:text-gray-400',
                  status === 'active' && 'text-blue-900 dark:text-blue-100',
                  status === 'completed' && 'text-green-900 dark:text-green-100',
                  status === 'error' && 'text-red-900 dark:text-red-100'
                )}>
                  {step.label}
                </h3>
                <p className={clsx(
                  'text-sm transition-colors duration-300',
                  status === 'pending' && 'text-gray-400 dark:text-gray-500',
                  status === 'active' && 'text-blue-700 dark:text-blue-300',
                  status === 'completed' && 'text-green-700 dark:text-green-300',
                  status === 'error' && 'text-red-700 dark:text-red-300'
                )}>
                  {status === 'error' && index === currentStepIndex 
                    ? 'An error occurred during this step' 
                    : status === 'active' && index === currentStepIndex && state.currentStep
                    ? state.currentStep
                    : step.description}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Error handling */}
      {(state.status === 'error' || state.status === 'failed') && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
        >
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h4 className="text-sm font-medium text-red-900 dark:text-red-100">
                Generation Failed
              </h4>
              <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                {state.error || 'An unexpected error occurred during generation.'}
              </p>
            </div>
          </div>
          
          <div className="mt-4 flex space-x-3">
            <Button
              variant="outline"
              size="sm"
              onClick={onRetry}
              disabled={isGenerating()}
              className="border-red-300 dark:border-red-600 text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/30"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isGenerating() ? 'animate-spin' : ''}`} />
              {isGenerating() ? 'Generating...' : 'Try Again'}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearError}
              className="text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/30"
            >
              Dismiss
            </Button>
          </div>
        </motion.div>
      )}

      {/* Success message */}
      {state.status === 'completed' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-6 text-center"
        >
          <div className="inline-flex items-center space-x-2 text-green-600 dark:text-green-400">
            <CheckCircle className="h-5 w-5" />
            <span className="font-medium">Animation generated successfully!</span>
          </div>
          
          {state.completedTime && state.startTime && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Total time: {Math.round((state.completedTime.getTime() - state.startTime.getTime()) / 1000)}s
            </p>
          )}
        </motion.div>
      )}
    </div>
  );
}