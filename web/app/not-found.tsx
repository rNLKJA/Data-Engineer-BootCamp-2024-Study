import Link from "next/link";
import { Database } from "lucide-react";

export default function NotFound() {
  return (
    <div className="dark flex min-h-dvh flex-col items-center justify-center px-4">
      <div className="text-center">
        <Database className="mx-auto size-16 text-mint/40" aria-hidden="true" />
        <h1 className="mt-6 font-display text-4xl font-semibold tracking-tight">
          Pipeline not found
        </h1>
        <p className="mt-4 text-lg text-muted-foreground">
          That route doesn't exist yet. The curriculum is still being built, week by week.
        </p>
        <Link
          href="/"
          className="mt-8 inline-flex h-12 items-center gap-2 rounded-full bg-mint px-6 text-[0.95rem] font-medium text-graphite-deep transition-colors hover:bg-mint/90"
        >
          Back to curriculum
        </Link>
      </div>
      <footer className="mt-16 text-sm text-muted-foreground">
        <a
          href="https://rin.contact"
          className="text-mint underline-offset-4 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          Made by Rin in Adelaide
        </a>
      </footer>
    </div>
  );
}
