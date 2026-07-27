import React from "react";

interface PrisentIconProps {
  size?: number;
  color?: string;
  className?: string;
}

export function PrisentIcon({ size = 24, color = "#FAFAFA", className = "" }: PrisentIconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Vertical stem (2 units wide on left boundary with rounded cap) */}
      <rect x="0" y="0" width="2" height="16" rx="1" fill={color} />

      {/* Layered parallel loops (3 bands, each 2 units high, concentric corner radii) */}
      {/* Band 1 - Top curved loop */}
      <path
        d="M2 1H9C11.209 1 13 2.791 13 5C13 7.209 11.209 9 9 9H2V7H9C10.105 7 11 6.105 11 5C11 3.895 10.105 3 9 3H2V1Z"
        fill={color}
      />
      {/* Band 2 - Middle path */}
      <rect x="2" y="5" width="8" height="2" rx="1" fill={color} />
      {/* Band 3 - Bottom path */}
      <rect x="2" y="9" width="6" height="2" rx="1" fill={color} />
    </svg>
  );
}
