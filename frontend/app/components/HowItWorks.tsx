import { motion } from 'framer-motion';
import { MessageSquare, Cpu, Download, CheckCircle } from 'lucide-react';

export function HowItWorks() {
  const steps = [
    {
      number: '01',
      icon: <MessageSquare className="h-8 w-8" />,
      title: 'Describe Your Concept',
      description: 'Simply type what you want to animate in plain English. Be as specific or general as you like.',
      example: '"Show how the derivative of x² is 2x with a moving tangent line"',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      number: '02',
      icon: <Cpu className="h-8 w-8" />,
      title: 'AI Generates Animation',
      description: 'Our AI understands your request and generates professional Manim code automatically.',
      example: 'AI creates smooth animations with proper timing and visual hierarchy',
      color: 'from-purple-500 to-pink-500'
    },
    {
      number: '03',
      icon: <Download className="h-8 w-8" />,
      title: 'Export & Share',
      description: 'Download your animation as MP4, GIF, or get embed code for your website.',
      example: 'High-quality exports ready for presentations, videos, or online courses',
      color: 'from-green-500 to-emerald-500'
    }
  ];

  return (
    <section id="how-it-works" className="py-20 bg-white dark:bg-gray-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center space-x-2 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <CheckCircle className="h-4 w-4" />
            <span>Simple Process</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-gray-900 dark:text-white">How it works in</span>{' '}
            <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              3 simple steps
            </span>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Creating mathematical animations has never been easier. No coding skills required!
          </p>
        </motion.div>

        {/* Steps */}
        <div className="relative">
          {/* Connection line */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 via-purple-500 to-green-500 transform -translate-y-1/2" />

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-4">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="relative"
              >
                <div className="bg-white dark:bg-gray-900 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-800">
                  {/* Step number */}
                  <div className="flex items-center mb-4">
                    <div className="text-5xl font-bold text-gray-200 dark:text-gray-800 mr-4">
                      {step.number}
                    </div>
                    <div className={`p-3 rounded-lg bg-gradient-to-r ${step.color} text-white`}>
                      {step.icon}
                    </div>
                  </div>

                  {/* Content */}
                  <h3 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {step.description}
                  </p>

                  {/* Example */}
                  <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Example:</p>
                    <p className="text-sm font-mono text-gray-700 dark:text-gray-300">
                      {step.example}
                    </p>
                  </div>
                </div>

                {/* Connection dots for mobile */}
                {index < steps.length - 1 && (
                  <div className="lg:hidden flex justify-center my-4">
                    <div className="w-1 h-8 bg-gradient-to-b from-gray-300 to-gray-300 dark:from-gray-700 dark:to-gray-700" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>

        {/* Demo video placeholder */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-1">
            <div className="bg-white dark:bg-gray-950 rounded-xl p-8">
              <div className="aspect-video bg-gray-100 dark:bg-gray-900 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-4">
                    <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M6.3 2.841A1.5 1.5 0 004 4.11v11.78a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                    </svg>
                  </div>
                  <p className="text-gray-600 dark:text-gray-400 font-medium">
                    Watch ManimStudio in Action
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                    See how easy it is to create stunning mathematical animations
                  </p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}