"use client";

import { useEffect, useState } from "react";

/** Hero visual with rich abstract data pipeline artwork, floating Week 1 card, and progress indicator. */
export function HeroVisual() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Animate to 16.67% (1 out of 6 weeks)
    const timer = setTimeout(() => setProgress(16.67), 100);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative mx-auto w-full max-w-md lg:max-w-none">
      <div className="arch relative aspect-[4/5] w-full overflow-hidden border border-white/10 bg-gradient-to-br from-[#2a3442] to-[#242935] shadow-[0_20px_60px_-20px_rgba(92,225,181,0.25)]">
        {/* Abstract data pipeline SVG */}
        <svg
          viewBox="0 0 400 500"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="absolute inset-0 size-full"
          aria-hidden="true"
        >
          <defs>
            <radialGradient id="pipeline-glow-1" cx="0.5" cy="0.2">
              <stop offset="0%" stopColor="#d4f5ea" stopOpacity="0.8" />
              <stop offset="20%" stopColor="#b5f3e1" stopOpacity="0.6" />
              <stop offset="40%" stopColor="#8de8ca" stopOpacity="0.4" />
              <stop offset="70%" stopColor="#5ce1b5" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#3ab89f" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="pipeline-glow-2" cx="0.7" cy="0.8">
              <stop offset="0%" stopColor="#e8fdf7" stopOpacity="0.75" />
              <stop offset="30%" stopColor="#c7f3e6" stopOpacity="0.5" />
              <stop offset="50%" stopColor="#8de8ca" stopOpacity="0.3" />
              <stop offset="80%" stopColor="#5ce1b5" stopOpacity="0.15" />
              <stop offset="100%" stopColor="#3ab89f" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="pipeline-glow-3" cx="0.3" cy="0.5">
              <stop offset="0%" stopColor="#c7f3e6" stopOpacity="0.7" />
              <stop offset="30%" stopColor="#a5efd8" stopOpacity="0.5" />
              <stop offset="60%" stopColor="#5ce1b5" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#3ab89f" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="pipeline-glow-4" cx="0.6" cy="0.4">
              <stop offset="0%" stopColor="#e8fdf7" stopOpacity="0.65" />
              <stop offset="40%" stopColor="#a5efd8" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#5ce1b5" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="purple-glow" cx="0.3" cy="0.7">
              <stop offset="0%" stopColor="#e9d5ff" stopOpacity="0.7" />
              <stop offset="40%" stopColor="#d8b4fe" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#bd93f9" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="pink-glow" cx="0.8" cy="0.3">
              <stop offset="0%" stopColor="#ffd1e8" stopOpacity="0.6" />
              <stop offset="50%" stopColor="#f9a8d4" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#ff79c6" stopOpacity="0" />
            </radialGradient>
            <linearGradient id="stream-1" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#e8fdf7" stopOpacity="0.9" />
              <stop offset="25%" stopColor="#d4f5ea" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#a5efd8" stopOpacity="0.7" />
              <stop offset="75%" stopColor="#5ce1b5" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#3ab89f" stopOpacity="0.3" />
            </linearGradient>
            <linearGradient id="stream-2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ffd1e8" stopOpacity="0.85" />
              <stop offset="25%" stopColor="#f9a8d4" stopOpacity="0.75" />
              <stop offset="50%" stopColor="#ff79c6" stopOpacity="0.6" />
              <stop offset="75%" stopColor="#e879f9" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#bd93f9" stopOpacity="0.25" />
            </linearGradient>
            <linearGradient id="stream-3" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#c7f3e6" stopOpacity="0.95" />
              <stop offset="30%" stopColor="#a5efd8" stopOpacity="0.85" />
              <stop offset="60%" stopColor="#5ce1b5" stopOpacity="0.7" />
              <stop offset="85%" stopColor="#3ab89f" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#2ba88c" stopOpacity="0.35" />
            </linearGradient>
            <linearGradient id="column-fill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#e8fdf7" stopOpacity="0.95" />
              <stop offset="20%" stopColor="#d4f5ea" stopOpacity="0.9" />
              <stop offset="40%" stopColor="#b5f3e1" stopOpacity="0.85" />
              <stop offset="60%" stopColor="#8de8ca" stopOpacity="0.75" />
              <stop offset="80%" stopColor="#5ce1b5" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#3ab89f" stopOpacity="0.5" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="8" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <filter id="soft-glow">
              <feGaussianBlur stdDeviation="12" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <filter id="noise">
              <feTurbulence
                type="fractalNoise"
                baseFrequency="0.65"
                numOctaves="5"
                seed="42"
                result="noise"
              />
              <feColorMatrix in="noise" type="saturate" values="0" result="desaturatedNoise" />
              <feComponentTransfer in="desaturatedNoise" result="theNoise">
                <feFuncA type="linear" slope="0.15" />
              </feComponentTransfer>
              <feBlend in="SourceGraphic" in2="theNoise" mode="soft-light" />
            </filter>
          </defs>

          {/* Background ambient glow layers */}
          <rect width="400" height="500" fill="url(#pipeline-glow-1)" />
          <rect width="400" height="500" fill="url(#pipeline-glow-2)" />
          <rect width="400" height="500" fill="url(#pipeline-glow-3)" />
          <rect width="400" height="500" fill="url(#pipeline-glow-4)" />
          <rect width="400" height="500" fill="url(#purple-glow)" />
          <rect width="400" height="500" fill="url(#pink-glow)" />

          {/* Flowing data streams converging into a central column */}
          <g filter="url(#glow)">
            {/* Left stream - multiple layers for depth */}
            <path
              d="M 60 80 Q 100 140, 140 200 Q 160 240, 180 300 L 190 400"
              stroke="url(#stream-1)"
              strokeWidth="24"
              strokeLinecap="round"
              fill="none"
              opacity="0.6"
            />
            <path
              d="M 60 80 Q 100 140, 140 200 Q 160 240, 180 300 L 190 400"
              stroke="url(#stream-1)"
              strokeWidth="16"
              strokeLinecap="round"
              fill="none"
              opacity="0.85"
            />
            <path
              d="M 60 80 Q 100 140, 140 200 Q 160 240, 180 300 L 190 400"
              stroke="url(#stream-1)"
              strokeWidth="6"
              strokeLinecap="round"
              fill="none"
              opacity="1"
            />

            {/* Right stream - rich layering */}
            <path
              d="M 340 60 Q 300 120, 260 180 Q 230 220, 210 280 L 200 400"
              stroke="url(#stream-2)"
              strokeWidth="22"
              strokeLinecap="round"
              fill="none"
              opacity="0.55"
            />
            <path
              d="M 340 60 Q 300 120, 260 180 Q 230 220, 210 280 L 200 400"
              stroke="url(#stream-2)"
              strokeWidth="14"
              strokeLinecap="round"
              fill="none"
              opacity="0.8"
            />
            <path
              d="M 340 60 Q 300 120, 260 180 Q 230 220, 210 280 L 200 400"
              stroke="url(#stream-2)"
              strokeWidth="5"
              strokeLinecap="round"
              fill="none"
              opacity="1"
            />

            {/* Center stream - dominant flow */}
            <path
              d="M 200 100 L 195 400"
              stroke="url(#stream-3)"
              strokeWidth="28"
              strokeLinecap="round"
              fill="none"
              opacity="0.6"
            />
            <path
              d="M 200 100 L 195 400"
              stroke="url(#stream-3)"
              strokeWidth="20"
              strokeLinecap="round"
              fill="none"
              opacity="0.8"
            />
            <path
              d="M 200 100 L 195 400"
              stroke="url(#stream-3)"
              strokeWidth="8"
              strokeLinecap="round"
              fill="none"
              opacity="1"
            />
          </g>

          {/* Secondary stream elements for richness */}
          <g opacity="0.6" filter="url(#soft-glow)">
            <path
              d="M 120 50 Q 150 100, 165 160"
              stroke="#bd93f9"
              strokeWidth="3"
              strokeLinecap="round"
              fill="none"
              opacity="0.7"
            />
            <path
              d="M 280 40 Q 250 90, 235 150"
              stroke="#ff79c6"
              strokeWidth="3"
              strokeLinecap="round"
              fill="none"
              opacity="0.6"
            />
          </g>

          {/* Data nodes along streams with glow */}
          <g filter="url(#soft-glow)">
            <circle cx="60" cy="80" r="10" fill="#5ce1b5" opacity="0.95" />
            <circle cx="60" cy="80" r="6" fill="#8de8ca" opacity="1" />

            <circle cx="140" cy="200" r="8" fill="#8de8ca" opacity="0.9" />
            <circle cx="140" cy="200" r="5" fill="#5ce1b5" opacity="1" />

            <circle cx="340" cy="60" r="9" fill="#ff79c6" opacity="0.9" />
            <circle cx="340" cy="60" r="5" fill="#ffd1e8" opacity="1" />

            <circle cx="260" cy="180" r="7" fill="#bd93f9" opacity="0.85" />
            <circle cx="260" cy="180" r="4" fill="#e9d5ff" opacity="1" />

            <circle cx="200" cy="100" r="12" fill="#5ce1b5" opacity="0.95" />
            <circle cx="200" cy="100" r="7" fill="#8de8ca" opacity="1" />

            <circle cx="180" cy="300" r="6" fill="#0d7377" opacity="0.8" />
            <circle cx="180" cy="300" r="3" fill="#5ce1b5" opacity="1" />
          </g>

          {/* Particle effects */}
          <g opacity="0.7">
            <circle cx="95" cy="110" r="2" fill="#8de8ca" opacity="0.9" />
            <circle cx="145" cy="170" r="1.5" fill="#5ce1b5" opacity="0.8" />
            <circle cx="300" cy="90" r="2" fill="#ff79c6" opacity="0.85" />
            <circle cx="240" cy="150" r="1.5" fill="#bd93f9" opacity="0.8" />
            <circle cx="195" cy="220" r="2" fill="#5ce1b5" opacity="0.9" />
          </g>

          {/* Central column (the pipeline output) - rich gradients */}
          <g filter="url(#glow)">
            <rect
              x="170"
              y="375"
              width="55"
              height="110"
              rx="10"
              fill="url(#column-fill)"
              opacity="0.7"
            />
            <rect
              x="175"
              y="380"
              width="45"
              height="100"
              rx="8"
              fill="url(#column-fill)"
              opacity="0.9"
            />
            <rect x="180" y="385" width="35" height="90" rx="6" fill="#8de8ca" opacity="0.6" />

            {/* Inner glow bands */}
            <rect x="183" y="395" width="29" height="15" rx="3" fill="#c7f3e6" opacity="0.8" />
            <rect x="183" y="425" width="29" height="12" rx="3" fill="#d4f5ea" opacity="0.75" />
            <rect x="183" y="450" width="29" height="10" rx="3" fill="#a5efd8" opacity="0.85" />
          </g>

          {/* Grain overlay with noise filter */}
          <rect width="400" height="500" fill="transparent" filter="url(#noise)" />

          {/* Vignette */}
          <rect
            width="400"
            height="500"
            fill="radial-gradient(ellipse at center, transparent 30%, rgba(10,13,18,0.6) 100%)"
            style={{ mixBlendMode: "multiply" }}
            opacity="0.7"
          />
        </svg>

        <div className="absolute inset-0 bg-gradient-to-t from-[#1a1f2e]/70 via-transparent to-transparent" />
      </div>

      {/* Progress indicator */}
      <div
        className="absolute bottom-0 left-0 right-0 h-1 overflow-hidden rounded-b-2xl bg-white/5"
        role="progressbar"
        aria-valuenow={1}
        aria-valuemin={0}
        aria-valuemax={6}
        aria-label="Course progress: 1 of 6 weeks complete"
      >
        <div
          className="h-full bg-gradient-to-r from-mint to-teal transition-all duration-1000 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Floating Week 1 card with shadow */}
      <div className="absolute -bottom-8 -left-2 w-[17rem] -rotate-3 sm:-left-10 sm:w-[19rem] rounded-2xl border border-white/10 bg-card/95 p-4 shadow-lg backdrop-blur">
        <div className="kicker text-mint">Week 1 · complete</div>
        <div className="mt-2 font-display text-xl font-semibold">
          Introduction &amp; Prerequisites
        </div>
        <ul className="mt-3 space-y-1.5 text-xs text-muted-foreground">
          <li className="flex items-start gap-2">
            <span className="mt-1 size-1 shrink-0 rounded-full bg-mint" />
            <span>Docker and docker-compose</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="mt-1 size-1 shrink-0 rounded-full bg-mint" />
            <span>Postgres with Docker</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="mt-1 size-1 shrink-0 rounded-full bg-mint" />
            <span>Infrastructure with Terraform</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
