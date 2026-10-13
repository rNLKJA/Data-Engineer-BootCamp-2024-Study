import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import "./globals.css";

// Self-hosted latin subsets from @fontsource-variable 5.3.0 (OFL; licences in
// ./fonts), so builds never depend on fetching Google Fonts.
const display = localFont({
  src: "./fonts/fraunces-latin-opsz-normal.woff2",
  variable: "--font-display-face",
  weight: "100 900",
  style: "normal",
  display: "swap",
});

const body = localFont({
  src: "./fonts/geist-latin-wght-normal.woff2",
  variable: "--font-body-face",
  weight: "100 900",
  style: "normal",
  display: "swap",
});

const mono = localFont({
  src: "./fonts/jetbrains-mono-latin-wght-normal.woff2",
  variable: "--font-code-face",
  weight: "100 800",
  style: "normal",
  display: "swap",
});

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#fafafa" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0d12" },
  ],
};

export const metadata: Metadata = {
  title: {
    default: "Data Engineer BootCamp",
    template: "%s · Data Engineer BootCamp",
  },
  description:
    "Learn data engineering fundamentals through hands-on curriculum spanning orchestration, warehousing, analytics, batch and stream processing.",
  openGraph: {
    title: "Data Engineer BootCamp",
    description:
      "Six weeks of hands-on data engineering training. Working through the DataTalksClub Zoomcamp, one week at a time.",
    type: "website",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Data Engineer BootCamp - Six weeks of hands-on training",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Data Engineer BootCamp",
    description: "Six weeks of hands-on data engineering training",
    images: ["/og-image.png"],
  },
  icons: {
    icon: [
      { url: "/favicon-16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon-32.png", sizes: "32x32", type: "image/png" },
    ],
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${display.variable} ${body.variable} ${mono.variable} h-full antialiased dark`}
    >
      <body className="flex min-h-full flex-col">
        <a
          href="#main"
          className="sr-only z-50 rounded-md bg-primary px-3 py-2 text-primary-foreground focus:not-sr-only focus:fixed focus:top-3 focus:left-3"
        >
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}
