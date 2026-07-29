import React from "react";

interface PrisentIconProps {
  size?: number;
  color?: string;
  className?: string;
}

export function PrisentIcon({ size = 16, color, className = "" }: PrisentIconProps) {
  return (
    <img
      src="/image-1.png"
      alt="Prisent Logo"
      className={`image-1 ${className}`}
      style={{
        width: size,
        height: size,
        objectFit: "contain",
      }}
    />
  );
}









