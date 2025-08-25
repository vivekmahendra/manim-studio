import * as React from 'react';
import { useSearchParams, Link } from 'react-router';
import { motion } from 'framer-motion';
import { ArrowLeft, RefreshCw, Share2, Home } from 'lucide-react';
import type { Route } from './+types/generate';

import { GenerationProvider, useGeneration, useGenerationURLState } from '~/contexts/GenerationContext';
import { GenerationProgress } from '~/components/GenerationProgress';
import { VideoPlayer } from '~/components/VideoPlayer';
import { CodeViewer } from '~/components/CodeViewer';
import { Button } from '~/components/ui/Button';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Generate Animation - ManimStudio" },
    { name: "description", content: "Watch your mathematical concept come to life with AI-generated animations." },
  ];
}

function GeneratePage() {
  const [searchParams] = useSearchParams();
  const { state, generateAnimation, reset, isGenerating } = useGeneration();

  // Initialize generation from URL
  React.useEffect(() => {
    const promptFromURL = searchParams.get('prompt');
    if (promptFromURL && state.status === 'idle') {
      generateAnimation(promptFromURL);
    }
  }, [searchParams, generateAnimation, state.status]);

  const handleRetry = React.useCallback(() => {
    if (state.prompt) {
      generateAnimation(state.prompt);
    }
  }, [state.prompt, generateAnimation]);

  const handleShare = React.useCallback(async () => {
    if (!state.result) return;
    
    const shareData = {
      title: 'Check out this math animation!',
      text: `Generated animation: "${state.prompt}"`,
      url: window.location.href
    };

    if (navigator.share && navigator.canShare?.(shareData)) {
      try {
        await navigator.share(shareData);
      } catch (error) {
        // Fallback to clipboard
        await navigator.clipboard.writeText(window.location.href);
      }
    } else {
      // Fallback to clipboard
      await navigator.clipboard.writeText(window.location.href);
    }
  }, [state.result, state.prompt]);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link 
                to="/"
                className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                <ArrowLeft className="h-5 w-5" />
                <span>Back to Home</span>
              </Link>
            </div>

            <div className="flex items-center space-x-3">
              {state.result && (
                <Button variant="outline" size="sm" onClick={handleShare}>
                  <Share2 className="h-4 w-4 mr-2" />
                  Share
                </Button>
              )}
              
              <Button variant="outline" size="sm" onClick={reset}>
                <Home className="h-4 w-4 mr-2" />
                New Animation
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Progress Section */}
          {(state.status !== 'idle' && state.status !== 'completed') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-center"
            >
              <GenerationProgress onRetry={handleRetry} />
            </motion.div>
          )}

          {/* Results Section */}
          {state.status === 'completed' && state.result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="space-y-8"
            >
              {/* Success Header */}
              <div className="text-center">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
                  Your Animation is Ready! 🎉
                </h1>
                <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
                  "{state.prompt}"
                </p>
              </div>

              {/* Video Player */}
              <div className="max-w-4xl mx-auto">
                <div className="bg-white dark:bg-gray-900 rounded-xl shadow-lg overflow-hidden">
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                        Generated Animation
                      </h2>
                      <div className="flex items-center space-x-4">
                        <span className="text-sm text-gray-500 dark:text-gray-400">
                          Scene: {state.result.scene_name}
                        </span>
                        
                        {/* Generation Method Indicator */}
                        {state.result.method === 'openai_generated' ? (
                          <div className="flex items-center space-x-1 px-2 py-1 bg-green-100 dark:bg-green-900/20 rounded-full">
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span className="text-xs font-medium text-green-700 dark:text-green-300">
                              AI Generated
                            </span>
                          </div>
                        ) : state.result.method === 'sample_fallback' || state.result.method === 'emergency_fallback' ? (
                          <div className="flex items-center space-x-1 px-2 py-1 bg-yellow-100 dark:bg-yellow-900/20 rounded-full">
                            <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                            <span className="text-xs font-medium text-yellow-700 dark:text-yellow-300">
                              Sample Content
                            </span>
                          </div>
                        ) : null}
                      </div>
                    </div>
                    
                    <VideoPlayer 
                      src={state.result.video_url}
                      title={state.result.scene_name}
                      autoPlay={false}
                      onError={(error) => console.error('Video error:', error)}
                    />
                    
                    {state.result.description && (
                      <p className="mt-4 text-gray-600 dark:text-gray-400 text-center">
                        {state.result.description}
                      </p>
                    )}
                    
                    {/* Sample content warning */}
                    {(state.result.method === 'sample_fallback' || state.result.method === 'emergency_fallback') && (
                      <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/10 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                        <p className="text-sm text-yellow-800 dark:text-yellow-200 text-center">
                          ⚠️ This is sample content shown because AI generation temporarily failed. 
                          {state.result.sample_used && ` (Sample: ${state.result.sample_used})`}
                          <br />
                          <button 
                            onClick={handleRetry}
                            className="underline hover:no-underline font-medium mt-1"
                          >
                            Try generating again
                          </button> for AI-generated content.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Code Viewer */}
              <div className="max-w-6xl mx-auto">
                <CodeViewer 
                  code={state.result.code}
                  fileName={`${state.result.scene_name.toLowerCase()}.py`}
                  defaultExpanded={false}
                />
              </div>

              {/* Actions */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button 
                  variant="primary" 
                  size="lg"
                  onClick={handleRetry}
                  disabled={isGenerating()}
                >
                  <RefreshCw className={`h-5 w-5 mr-2 ${isGenerating() ? 'animate-spin' : ''}`} />
                  {isGenerating() ? 'Generating...' : 'Generate Another Version'}
                </Button>
                
                <Button 
                  variant="outline" 
                  size="lg"
                  onClick={reset}
                >
                  Create New Animation
                </Button>
              </div>
            </motion.div>
          )}

          {/* Empty state */}
          {state.status === 'idle' && !searchParams.get('prompt') && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center py-16"
            >
              <div className="max-w-md mx-auto">
                <div className="text-6xl mb-6">🎬</div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  No Animation in Progress
                </h1>
                <p className="text-gray-600 dark:text-gray-400 mb-8">
                  Start by entering a prompt on the home page to generate your first animation.
                </p>
                <Link to="/">
                  <Button variant="primary" size="lg">
                    <Home className="h-5 w-5 mr-2" />
                    Go to Home Page
                  </Button>
                </Link>
              </div>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  );
}

// Export with provider
export default function Generate() {
  return (
    <GenerationProvider>
      <GeneratePage />
    </GenerationProvider>
  );
}