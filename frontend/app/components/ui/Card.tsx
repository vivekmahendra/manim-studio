import * as React from 'react';
import { clsx } from 'clsx';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glass?: boolean;
}

export function Card({ children, className, hover = false, glass = false }: CardProps) {
  const baseStyles = 'rounded-xl overflow-hidden transition-all duration-300';
  
  const defaultStyles = glass
    ? 'bg-white/10 backdrop-blur-md border border-white/20 dark:bg-gray-900/10 dark:border-gray-700/20'
    : 'bg-white border border-gray-200 dark:bg-gray-900 dark:border-gray-800';
  
  const hoverStyles = hover
    ? 'hover:shadow-xl hover:scale-[1.02] cursor-pointer'
    : '';
  
  return (
    <div className={clsx(baseStyles, defaultStyles, hoverStyles, className)}>
      {children}
    </div>
  );
}