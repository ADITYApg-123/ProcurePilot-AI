import React from 'react';
import './ui.css';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: 'default' | 'glass';
}

export function Card({ children, className = '', variant = 'glass', ...props }: CardProps) {
  const baseClass = variant === 'glass' ? 'glass-panel' : 'card-default';
  return (
    <div className={`${baseClass} ${className}`} {...props}>
      {children}
    </div>
  );
}
