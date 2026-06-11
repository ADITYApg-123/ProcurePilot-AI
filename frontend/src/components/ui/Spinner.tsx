import React from 'react';
import './ui.css';

interface SpinnerProps {
  size?: number;
  className?: string;
}

export function Spinner({ size = 24, className = '' }: SpinnerProps) {
  return (
    <div 
      className={`spinner-circle ${className}`} 
      style={{ width: size, height: size }}
    />
  );
}
