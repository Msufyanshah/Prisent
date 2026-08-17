import React from "react";

interface PrisentIconProps {
  size?: number;
  color?: string;
  className?: string;
}

export function PrisentIcon({ size = 24, className = "" }: PrisentIconProps) {
  return (
    <img
      src="/image-1.png"
      alt="Prisent Logo"
      width={size}
      height={size}
      className={className}
      style={{
        objectFit: "contain",
        borderRadius: "8px"
      }}
    />
  );
}









