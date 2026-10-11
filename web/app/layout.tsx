import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f8f8f8" },
    { media: "(prefers-color-scheme: dark)", color: "#0f172a" },
  ],
};

export const metadata: Metadata = {
  title: "Data Engineer BootCamp",
  description:
    "Learn data engineering fundamentals through hands-on curriculum spanning orchestration, warehousing, analytics, batch and stream processing.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full antialiased scroll-smooth">
      <body className="flex min-h-full flex-col bg-background text-foreground">
        <header className="sticky top-0 z-50 border-b border-card-border bg-card-bg/95 backdrop-blur supports-[backdrop-filter]:bg-card-bg/75">
          <nav className="mx-auto max-w-7xl flex items-center justify-between px-6 py-4 sm:px-8">
            <a href="/" className="text-lg font-semibold tracking-tight text-foreground">
              Data Engineer BootCamp
            </a>
            <div className="flex gap-6 text-sm">
              <a href="/" className="text-foreground hover:text-slate transition-colors">
                Home
              </a>
              <a
                href="https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study"
                target="_blank"
                rel="noopener noreferrer"
                className="text-foreground hover:text-slate transition-colors"
              >
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
