import { Sparkles, Github, Twitter, Linkedin, Mail, Heart } from 'lucide-react';
import { Input } from './ui/Input';
import { Button } from './ui/Button';

export function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    Product: [
      { label: 'Features', href: '#features' },
      { label: 'Examples', href: '#examples' },
      { label: 'Pricing', href: '#pricing' },
      { label: 'API Access', href: '#' }
    ],
    Resources: [
      { label: 'Documentation', href: '#' },
      { label: 'Tutorials', href: '#' },
      { label: 'Blog', href: '#' },
      { label: 'Community', href: '#' }
    ],
    Company: [
      { label: 'About Us', href: '#' },
      { label: 'Careers', href: '#' },
      { label: 'Contact', href: '#' },
      { label: 'Partners', href: '#' }
    ],
    Legal: [
      { label: 'Privacy Policy', href: '#' },
      { label: 'Terms of Service', href: '#' },
      { label: 'Cookie Policy', href: '#' },
      { label: 'License', href: '#' }
    ]
  };

  const socialLinks = [
    { icon: <Github className="h-5 w-5" />, href: '#', label: 'GitHub' },
    { icon: <Twitter className="h-5 w-5" />, href: '#', label: 'Twitter' },
    { icon: <Linkedin className="h-5 w-5" />, href: '#', label: 'LinkedIn' }
  ];

  return (
    <footer className="bg-gray-900 text-gray-300">
      {/* Newsletter section */}
      <div className="border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-bold text-white mb-2">
                Stay updated with ManimStudio
              </h3>
              <p className="text-gray-400">
                Get the latest features, tutorials, and math animation tips delivered to your inbox.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4">
              <Input
                type="email"
                placeholder="Enter your email"
                className="flex-1 bg-gray-800 border-gray-700 text-white placeholder-gray-500"
              />
              <Button variant="primary" size="md">
                Subscribe
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main footer content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Brand section */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Sparkles className="h-8 w-8 text-blue-500" />
              <span className="text-xl font-bold text-white">ManimStudio</span>
            </div>
            <p className="text-gray-400 mb-6">
              Transform mathematical concepts into beautiful animations with the power of AI and Manim.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  aria-label={social.label}
                  className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors duration-200"
                >
                  {social.icon}
                </a>
              ))}
            </div>
          </div>

          {/* Links sections */}
          {Object.entries(footerLinks).map(([title, links]) => (
            <div key={title}>
              <h4 className="font-semibold text-white mb-4">{title}</h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="text-gray-400 hover:text-white transition-colors duration-200"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom section */}
        <div className="mt-12 pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-1 text-gray-400">
              <span>© {currentYear} ManimStudio. Made with</span>
              <Heart className="h-4 w-4 text-red-500 fill-current" />
              <span>for educators</span>
            </div>
            <div className="flex items-center space-x-6 text-sm">
              <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                Status
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                API
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                Support
              </a>
              <a href="mailto:hello@manimstudio.com" className="flex items-center space-x-1 text-gray-400 hover:text-white transition-colors duration-200">
                <Mail className="h-4 w-4" />
                <span>Contact</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}