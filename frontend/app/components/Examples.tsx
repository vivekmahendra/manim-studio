import * as React from 'react';
import { motion } from 'framer-motion';
import { Play, Clock, Tag, Loader2 } from 'lucide-react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { api, type ExampleItem } from '~/services/api';

export function Examples() {
  const [activeCategory, setActiveCategory] = React.useState('all');
  const [examples, setExamples] = React.useState<ExampleItem[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  // Load examples from API
  React.useEffect(() => {
    const loadExamples = async () => {
      try {
        setLoading(true);
        const response = await api.getExamples();
        setExamples(response.examples);
        setError(null);
      } catch (error) {
        console.error('Failed to load examples:', error);
        setError('Failed to load examples');
      } finally {
        setLoading(false);
      }
    };

    loadExamples();
  }, []);

  const categories = React.useMemo(() => {
    if (examples.length === 0) {
      return [
        { id: 'all', label: 'All Examples' },
        { id: 'algebra', label: 'Algebra' },
        { id: 'geometry', label: 'Geometry' },
        { id: 'calculus', label: 'Calculus' },
        { id: 'physics', label: 'Physics' }
      ];
    }
    
    const uniqueCategories = [...new Set(examples.map(ex => ex.category))];
    return [
      { id: 'all', label: 'All Examples' },
      ...uniqueCategories.map(cat => ({
        id: cat,
        label: cat.charAt(0).toUpperCase() + cat.slice(1)
      }))
    ];
  }, [examples]);

  const filteredExamples = React.useMemo(() => {
    return activeCategory === 'all' 
      ? examples 
      : examples.filter(ex => ex.category === activeCategory);
  }, [examples, activeCategory]);

  return (
    <section id="examples" className="py-20 bg-gray-50 dark:bg-gray-900/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center space-x-2 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <Play className="h-4 w-4" />
            <span>Example Gallery</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-gray-900 dark:text-white">See what's possible with</span>{' '}
            <span className="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
              ManimStudio
            </span>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Explore our gallery of animations created from simple text prompts
          </p>
        </motion.div>

        {/* Category filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          viewport={{ once: true }}
          className="flex flex-wrap justify-center gap-2 mb-12"
        >
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                activeCategory === cat.id
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </motion.div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center py-16">
            <div className="flex flex-col items-center">
              <Loader2 className="h-8 w-8 animate-spin text-blue-600 mb-4" />
              <p className="text-gray-600 dark:text-gray-400">Loading examples...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-16">
            <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <Button onClick={() => window.location.reload()} variant="outline">
              Try Again
            </Button>
          </div>
        )}

        {/* Examples grid */}
        {!loading && !error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {filteredExamples.map((example, index) => (
            <motion.div
              key={`${example.title}-${index}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <Card hover className="overflow-hidden h-full flex flex-col">
                {/* Thumbnail */}
                <div className="relative aspect-video bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/20 dark:to-purple-900/20">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                      <div className="inline-flex items-center justify-center w-16 h-16 bg-white/80 dark:bg-gray-900/80 rounded-full mb-2">
                        <Play className="h-8 w-8 text-blue-600" />
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Click to preview</p>
                    </div>
                  </div>
                  
                  {/* Duration badge */}
                  <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-xs flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {example.duration}
                  </div>

                  {/* Category badge */}
                  <div className="absolute top-2 left-2 bg-white/90 dark:bg-gray-900/90 text-gray-700 dark:text-gray-300 px-2 py-1 rounded text-xs flex items-center gap-1">
                    <Tag className="h-3 w-3" />
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
                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">Prompt used:</p>
                    <p className="text-xs font-mono text-gray-700 dark:text-gray-300">
                      "{example.prompt}"
                    </p>
                  </div>

                  <a href={`/generate?prompt=${encodeURIComponent(example.prompt)}`}>
                    <Button variant="outline" size="sm" className="w-full">
                      Try This Prompt
                    </Button>
                  </a>
                </div>
              </Card>
            </motion.div>
          ))}
          </motion.div>
        )}

        {/* Empty state for filtered results */}
        {!loading && !error && filteredExamples.length === 0 && (
          <div className="text-center py-16">
            <p className="text-gray-600 dark:text-gray-400 text-lg mb-4">
              No examples found for "{activeCategory}" category.
            </p>
            <Button onClick={() => setActiveCategory('all')} variant="outline">
              Show All Examples
            </Button>
          </div>
        )}

        {/* CTA */}
        {!loading && !error && examples.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
            className="text-center mt-12"
          >
            <a href="/generate">
              <Button variant="primary" size="lg">
                Create Your Own Animation
              </Button>
            </a>
          </motion.div>
        )}
      </div>
    </section>
  );
}