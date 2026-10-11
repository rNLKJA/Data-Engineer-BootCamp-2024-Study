import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "Data Engineer BootCamp",
  description: "Learn data engineering fundamentals through hands-on curriculum spanning orchestration, warehousing, analytics, batch and stream processing.",
};

export default function RootLayout({ children }: {children: React.ReactNode}) {
  return (
    <html lang="en" className="h-full antialiased scroll-smooth">
      <body className="min-h-full flex flex-col bg-white text-black">
        <header className="border-b border-gray-300 sticky top-0 bg-white z-50">
          <nav className="mx-auto max-w-5xl flex items-center justify-between px-4 py-4">
            <a href="/" className="text-xl font-black">
              Data Engineer BootCamp
            </a>
            <div className="flex gap-4 text-sm">
              <a href="/" className="hover:text-gray-600">Home</a>
              <a href="https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study" target="_blank" rel="noopener noreferrer" className="hover:text-gray-600">
                GitHub
              </a>
            </div>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
