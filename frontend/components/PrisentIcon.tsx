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
      {/* Vertical stem (1X width / 2 units wide on left boundary) */}
      <rect x="0" y="0" width="2" height="16" fill={color} />

      {/* Layered pathway loops (3 parallel bands, 2 units high, 2 units gap, outer concentric radius) */}
      {/* Band 1 - Top path (y=0 to y=2) */}
      <path
        d="M2 0H10C12.2091 0 14 1.79086 14 4C14 6.20914 12.2091 8 10 8H2V6H10C11.1046 6 12 5.10457 12 4C12 2.89543 11.1046 2 10 2H2V0Z"
        fill={color}
      />
      {/* Band 2 - Middle path (y=4 to y=6) */}
      <rect x="2" y="4" width="8" height="2" fill={color} />
      {/* Band 3 - Bottom path (y=8 to y=10) */}
      <rect x="2" y="8" width="6" height="2" fill={color} />
    </svg>
  );
}
