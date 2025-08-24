import * as React from 'react';
import { motion } from 'framer-motion';
import { Play, Clock, Tag } from 'lucide-react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';

export function Examples() {
  const [activeCategory, setActiveCategory] = React.useState('all');

  const categories = [
    { id: 'all', label: 'All Examples' },
    { id: 'algebra', label: 'Algebra' },
    { id: 'geometry', label: 'Geometry' },
    { id: 'calculus', label: 'Calculus' },
    { id: 'physics', label: 'Physics' }
  ];

  const examples = [
    {
      id: 1,
      title: 'Vector Addition & Subtraction',
      category: 'algebra',
      duration: '45s',
      thumbnail: '/api/placeholder/400/225',
      description: 'Visual demonstration of vector operations in 2D space',
      prompt: 'Show how vectors add and subtract with animated arrows'
    },
    {
      id: 2,
      title: 'Hyperbola & Foci',
      category: 'geometry',
      duration: '60s',
      thumbnail: '/api/placeholder/400/225',
      description: 'Interactive visualization of hyperbola properties',
      prompt: 'Animate a hyperbola showing its foci and asymptotes'
    },
    {
      id: 3,
      title: 'Derivative Visualization',
      category: 'calculus',
      duration: '90s',
      thumbnail: '/api/placeholder/400/225',
      description: 'Tangent line moving along a curve',
      prompt: 'Show the derivative of x² with a moving tangent line'
    },
    {
      id: 4,
      title: 'Pythagorean Theorem',
      category: 'geometry',
      duration: '30s',
      thumbnail: '/api/placeholder/400/225',
      description: 'Classic proof with area visualization',
      prompt: 'Animate the Pythagorean theorem proof using squares'
    },
    {
      id: 5,
      title: 'Simple Harmonic Motion',
      category: 'physics',
      duration: '75s',
      thumbnail: '/api/placeholder/400/225',
      description: 'Oscillating spring and sine wave connection',
      prompt: 'Show simple harmonic motion with spring and graph'
    },
    {
      id: 6,
      title: 'Matrix Multiplication',
      category: 'algebra',
      duration: '50s',
      thumbnail: '/api/placeholder/400/225',
      description: 'Step-by-step matrix multiplication',
      prompt: 'Visualize 3x3 matrix multiplication step by step'
    }
  ];

  const filteredExamples = activeCategory === 'all' 
    ? examples 
    : examples.filter(ex => ex.category === activeCategory);

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

        {/* Examples grid */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {filteredExamples.map((example, index) => (
            <motion.div
              key={example.id}
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

                  <Button variant="outline" size="sm" className="w-full">
                    View Details
                  </Button>
                </div>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <Button variant="primary" size="lg">
            Create Your Own Animation
          </Button>
        </motion.div>
      </div>
    </section>
  );
}