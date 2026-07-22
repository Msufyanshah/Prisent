import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Prisent - Proactive Execution Platform",
  description: "AI-native infrastructure that turns ideas into execution.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-textPrimary antialiased selection:bg-accent selection:text-background min-h-screen">
        {children}
      </body>
    </html>
  );
}
