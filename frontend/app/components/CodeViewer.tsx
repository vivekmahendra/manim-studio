import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, Copy, Check, Download, Code2 } from 'lucide-react';
import { clsx } from 'clsx';
import { Button } from './ui/Button';

interface CodeViewerProps {
  code: string;
  language?: string;
  fileName?: string;
  className?: string;
  defaultExpanded?: boolean;
}

export function CodeViewer({ 
  code, 
  language = 'python',
  fileName = 'animation.py',
  className,
  defaultExpanded = false 
}: CodeViewerProps) {
  const [isExpanded, setIsExpanded] = React.useState(defaultExpanded);
  const [isCopied, setIsCopied] = React.useState(false);
  const [highlightedCode, setHighlightedCode] = React.useState<string>('');

  // Simple syntax highlighting for Python/Manim
  const highlightPython = React.useCallback((code: string): string => {
    // First, escape HTML entities to prevent issues
    let highlighted = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
    
    // Keywords
    const keywords = [
      'class', 'def', 'if', 'else', 'elif', 'for', 'while', 'import', 'from', 'as',
      'return', 'try', 'except', 'finally', 'with', 'lambda', 'and', 'or', 'not',
      'True', 'False', 'None', 'self'
    ];
    
    keywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      highlighted = highlighted.replace(regex, `<span class="text-purple-600 dark:text-purple-400 font-semibold">${keyword}</span>`);
    });
    
    // Manim classes and functions
    const manimKeywords = [
      'Scene', 'Create', 'Write', 'FadeIn', 'FadeOut', 'Transform', 'MathTex', 'Text',
      'Circle', 'Rectangle', 'Arrow', 'Dot', 'Line', 'VGroup', 'Axes', 'play', 'wait',
      'add', 'remove', 'construct'
    ];
    
    manimKeywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      highlighted = highlighted.replace(regex, `<span class="text-blue-600 dark:text-blue-400 font-medium">${keyword}</span>`);
    });
    
    // Strings (need to handle escaped quotes)
    highlighted = highlighted.replace(
      /(&#x27;)((?:(?!&#x27;)[^\\]|\\.)*)(\1)/g,
      '<span class="text-green-600 dark:text-green-400">$1$2$3</span>'
    );
    highlighted = highlighted.replace(
      /(&quot;)((?:(?!&quot;)[^\\]|\\.)*)(|&quot;)/g,
      '<span class="text-green-600 dark:text-green-400">$1$2$3</span>'
    );
    
    // Comments
    highlighted = highlighted.replace(
      /(#.*$)/gm,
      '<span class="text-gray-500 dark:text-gray-400 italic">$1</span>'
    );
    
    // Numbers
    highlighted = highlighted.replace(
      /\b(\d+(?:\.\d+)?)\b/g,
      '<span class="text-orange-600 dark:text-orange-400">$1</span>'
    );
    
    return highlighted;
  }, []);

  React.useEffect(() => {
    const highlighted = language === 'python' ? highlightPython(code) : code;
    setHighlightedCode(highlighted);
  }, [code, language, highlightPython]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy code:', error);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
  };

  const lineCount = code.split('\n').length;
  const previewLines = 10;
  const previewCode = isExpanded ? code : code.split('\n').slice(0, previewLines).join('\n');
  const previewHighlighted = isExpanded ? highlightedCode : highlightPython(previewCode);

  return (
    <div className={clsx('border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden', className)}>
      {/* Header */}
      <div className="bg-gray-50 dark:bg-gray-900 px-4 py-3 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Code2 className="h-5 w-5 text-gray-600 dark:text-gray-400" />
          <div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-white">
              Generated Manim Code
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {fileName} • {lineCount} lines
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleCopy}
            className="text-xs"
          >
            {isCopied ? (
              <>
                <Check className="h-4 w-4 mr-1" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="h-4 w-4 mr-1" />
                Copy
              </>
            )}
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={handleDownload}
            className="text-xs"
          >
            <Download className="h-4 w-4 mr-1" />
            Download
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-xs"
          >
            {isExpanded ? (
              <>
                <ChevronUp className="h-4 w-4 mr-1" />
                Collapse
              </>
            ) : (
              <>
                <ChevronDown className="h-4 w-4 mr-1" />
                Expand
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Code content */}
      <div className="relative">
        <AnimatePresence>
          <motion.div
            key={isExpanded ? 'expanded' : 'collapsed'}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className={clsx(
              'bg-gray-50 dark:bg-gray-900 overflow-auto',
              isExpanded ? 'max-h-96' : 'max-h-60'
            )}
          >
            <pre className="p-4 text-sm leading-relaxed">
              <code 
                className="text-gray-900 dark:text-gray-100 font-mono"
                dangerouslySetInnerHTML={{ __html: previewHighlighted }}
              />
            </pre>
          </motion.div>
        </AnimatePresence>

        {/* Fade overlay when collapsed */}
        {!isExpanded && lineCount > previewLines && (
          <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-gray-50 dark:from-gray-900 to-transparent pointer-events-none" />
        )}

        {/* Expand prompt */}
        {!isExpanded && lineCount > previewLines && (
          <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsExpanded(true)}
              className="text-xs bg-white dark:bg-gray-800 shadow-sm"
            >
              Show {lineCount - previewLines} more lines
              <ChevronDown className="h-3 w-3 ml-1" />
            </Button>
          </div>
        )}
      </div>

      {/* Code info */}
      <div className="bg-gray-50 dark:bg-gray-900 px-4 py-2 border-t border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center space-x-4">
            <span>Language: {language.charAt(0).toUpperCase() + language.slice(1)}</span>
            <span>Size: {(code.length / 1024).toFixed(1)} KB</span>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Ready to use</span>
          </div>
        </div>
      </div>
    </div>
  );
}