import React from 'react';

interface CohortlyLogoProps {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  className?: string;
}

export const CohortlyLogo: React.FC<CohortlyLogoProps> = ({ 
  size = 'md', 
  showText = true,
  className = '' 
}) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16'
  };

  const textSizeClasses = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-3xl'
  };

  return (
    <div className={`flex items-center ${className}`}>
      {/* Logo SVG */}
      <div className={`${sizeClasses[size]} relative`}>
        <svg
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full"
        >
          {/* Top chevron - Light teal */}
          <path
            d="M50 15 L85 35 L50 55 L15 35 Z"
            fill="#2DD4BF"
            className="drop-shadow-sm"
          />
          <circle cx="50" cy="25" r="5" fill="white" />
          <path
            d="M50 20 L50 30"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M48 27 L50 30 L52 27"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />

          {/* Middle chevron - Medium blue */}
          <path
            d="M50 35 L85 55 L50 75 L15 55 Z"
            fill="#06B6D4"
            className="drop-shadow-sm"
          />
          <circle cx="50" cy="45" r="5" fill="white" />
          <path
            d="M50 40 L50 50"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M48 47 L50 50 L52 47"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />

          {/* Bottom chevron - Dark blue */}
          <path
            d="M50 55 L85 75 L50 95 L15 75 Z"
            fill="#0284C7"
            className="drop-shadow-md"
          />
          <circle cx="50" cy="65" r="5" fill="white" />
          <path
            d="M50 60 L50 70"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <path
            d="M48 67 L50 70 L52 67"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </svg>
      </div>

      {/* Brand Name */}
      {showText && (
        <div className={`ml-3 font-bold ${textSizeClasses[size]}`}>
          <span className="text-gray-900">
            C<span className="text-sky-500">o</span>h<span className="text-sky-500">o</span>rtly
          </span>
        </div>
      )}
    </div>
  );
};

export default CohortlyLogo;
