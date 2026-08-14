import React from "react";

interface PrisentIconProps {
  size?: number;
  color?: string;
  className?: string;
}

export function PrisentIcon({ size = 24, color = "currentColor", className = "" }: PrisentIconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <rect width="32" height="32" rx="8" fill="url(#prisent-grad)" />
      <path
        d="M10 8H18.5C21.5376 8 24 10.4624 24 13.5C24 16.5376 21.5376 19 18.5 19H14V24H10V8ZM14 12V15H18.5C19.3284 15 20 14.3284 20 13.5C20 12.6716 19.3284 12 18.5 12H14Z"
        fill="#FFFFFF"
      />
      <defs>
        <linearGradient
          id="prisent-grad"
          x1="0"
          y1="0"
          x2="32"
          y2="32"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#6366F1" />
          <stop offset="1" stopColor="#A855F7" />
        </linearGradient>
      </defs>
    </svg>
  );
}









