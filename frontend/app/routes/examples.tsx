import * as React from 'react';
import { Link } from 'react-router';
import { motion } from 'framer-motion';
import { ArrowLeft, Play, ExternalLink } from 'lucide-react';
import type { Route } from './+types/examples';

import { api, type ExampleItem } from '~/services/api';
import { Button } from '~/components/ui/Button';
import { Card } from '~/components/ui/Card';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Examples - ManimStudio" },
    { name: "description", content: "Explore our gallery of mathematical animations created with ManimStudio." },
  ];
}

export default function Examples() {
  const [examples, setExamples] = React.useState<ExampleItem[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [filter, setFilter] = React.useState<string>('all');

  // Load examples from API
  React.useEffect(() => {
    const loadExamples = async () => {
      try {
        setLoading(true);
        const response = await api.getExamples();
        setExamples(response.examples);
      } catch (error) {
        setError(error instanceof Error ? error.message : 'Failed to load examples');
      } finally {
        setLoading(false);
      }
    };

    loadExamples();
  }, []);

  const categories = React.useMemo(() => {
    const cats = ['all', ...new Set(examples.map(ex => ex.category))];
    return cats;
  }, [examples]);

  const filteredExamples = React.useMemo(() => {
    return filter === 'all' 
      ? examples 
      : examples.filter(ex => ex.category === filter);
  }, [examples, filter]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading examples...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <Link 
                to="/"
                className="inline-flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mb-4"
              >
                <ArrowLeft className="h-5 w-5" />
                <span>Back to Home</span>
              </Link>
              
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Animation Examples
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Explore mathematical concepts brought to life with ManimStudio
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="flex flex-wrap gap-2 mb-8">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setFilter(category)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                filter === category
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>

        {/* Examples Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredExamples.map((example, index) => (
            <motion.div
              key={`${example.title}-${index}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <Card hover className="h-full flex flex-col">
                {/* Video thumbnail */}
                <div className="relative aspect-video bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="bg-white/20 backdrop-blur-md rounded-full p-4 group-hover:bg-white/30 transition-all duration-200">
                      <Play className="h-8 w-8 text-blue-600" />
                    </div>
                  </div>
                  
                  {/* Duration and category badges */}
                  <div className="absolute top-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
                    {example.duration}
                  </div>
                  <div className="absolute top-2 right-2 bg-white/90 dark:bg-gray-900/90 text-gray-700 dark:text-gray-300 px-2 py-1 rounded text-xs">
                    {example.category}
                  </div>
                </div>

                {/* Content */}
                <div className="p-6 flex-grow flex flex-col">
                  <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
                    {example.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 flex-grow">
                    {example.description}
                  </p>
                  
                  {/* Prompt preview */}
                  <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-4">
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Prompt:</p>
                    <p className="text-xs font-mono text-gray-700 dark:text-gray-300">
                      "{example.prompt}"
                    </p>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Link 
                      to={`/generate?prompt=${encodeURIComponent(example.prompt)}`}
                      className="flex-1"
                    >
                      <Button variant="primary" size="sm" className="w-full">
                        Try This Prompt
                      </Button>
                    </Link>
                    
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => window.open(example.video_url, '_blank')}
                    >
                      <ExternalLink className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredExamples.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-600 dark:text-gray-400 text-lg">
              No examples found for "{filter}" category.
            </p>
          </div>
        )}
      </main>
    </div>
  );
}