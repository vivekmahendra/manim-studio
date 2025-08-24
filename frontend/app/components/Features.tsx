import { motion } from 'framer-motion';
import { 
  Sparkles, 
  Palette, 
  FileVideo, 
  Languages, 
  Eye, 
  BookOpen,
  Zap,
  Code2,
  Download
} from 'lucide-react';
import { Card } from './ui/Card';

export function Features() {
  const features = [
    {
      icon: <Languages className="h-8 w-8" />,
      title: 'Natural Language Input',
      description: 'Just describe what you want to animate in plain English. No coding required.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <Sparkles className="h-8 w-8" />,
      title: 'AI-Powered Generation',
      description: 'Our AI understands mathematical concepts and creates accurate, beautiful animations.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: <FileVideo className="h-8 w-8" />,
      title: 'Professional Quality',
      description: 'Export in HD quality with smooth animations powered by the Manim library.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: <Palette className="h-8 w-8" />,
      title: 'Customizable Styles',
      description: 'Choose from various themes and color schemes to match your brand or preference.',
      color: 'from-orange-500 to-red-500'
    },
    {
      icon: <Eye className="h-8 w-8" />,
      title: 'Real-time Preview',
      description: 'See your animations come to life instantly as you refine your prompts.',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: <BookOpen className="h-8 w-8" />,
      title: 'Educational Templates',
      description: 'Pre-built templates for common educational topics and mathematical concepts.',
      color: 'from-teal-500 to-blue-500'
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5
      }
    }
  };

  return (
    <section id="features" className="py-20 bg-gray-50 dark:bg-gray-900/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center space-x-2 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <Zap className="h-4 w-4" />
            <span>Powerful Features</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-gray-900 dark:text-white">Everything you need to create</span>
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              stunning math animations
            </span>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            From simple equations to complex visualizations, ManimStudio has all the tools 
            you need to bring mathematical concepts to life.
          </p>
        </motion.div>

        {/* Features grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => (
            <motion.div key={index} variants={itemVariants}>
              <Card hover className="h-full p-6">
                <div className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${feature.color} text-white mb-4`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Additional features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="mt-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white"
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <Code2 className="h-12 w-12 mx-auto mb-3" />
              <h4 className="font-semibold mb-1">Clean Manim Code</h4>
              <p className="text-white/80 text-sm">Export the generated Python code for further customization</p>
            </div>
            <div>
              <Download className="h-12 w-12 mx-auto mb-3" />
              <h4 className="font-semibold mb-1">Multiple Formats</h4>
              <p className="text-white/80 text-sm">Export as MP4, GIF, or embed directly in your content</p>
            </div>
            <div>
              <Zap className="h-12 w-12 mx-auto mb-3" />
              <h4 className="font-semibold mb-1">Lightning Fast</h4>
              <p className="text-white/80 text-sm">Generate complex animations in seconds, not hours</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}