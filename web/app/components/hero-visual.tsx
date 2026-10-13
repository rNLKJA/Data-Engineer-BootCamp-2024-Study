/** Hero visual with abstract data pipeline artwork and floating Week 1 card. */
export function HeroVisual() {
  return (
    <div className="relative mx-auto w-full max-w-md lg:max-w-none">
      <div className="arch relative aspect-[4/5] w-full overflow-hidden border border-white/10 bg-gradient-to-br from-[#0f131c] to-[#0a0d12] shadow-2xl shadow-mint/20">
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
              <stop offset="0%" stopColor="#5ce1b5" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#0d7377" stopOpacity="0" />
            </radialGradient>
            <radialGradient id="pipeline-glow-2" cx="0.3" cy="0.7">
              <stop offset="0%" stopColor="#0d7377" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#0a0d12" stopOpacity="0" />
            </radialGradient>
            <linearGradient id="stream-1" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#5ce1b5" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#0d7377" stopOpacity="0.2" />
            </linearGradient>
            <linearGradient id="stream-2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#8de8ca" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#0a4f55" stopOpacity="0.15" />
            </linearGradient>
            <linearGradient id="stream-3" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#5ce1b5" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#0d7377" stopOpacity="0.25" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="6" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <filter id="noise">
              <feTurbulence
                type="fractalNoise"
                baseFrequency="0.9"
                numOctaves="4"
                result="noise"
              />
              <feColorMatrix
                in="noise"
                type="saturate"
                values="0"
                result="desaturatedNoise"
              />
              <feComponentTransfer in="desaturatedNoise" result="theNoise">
                <feFuncA type="discrete" tableValues="0 0 0 0 0 1" />
              </feComponentTransfer>
              <feBlend in="SourceGraphic" in2="theNoise" mode="overlay" />
            </filter>
          </defs>

          {/* Background glow */}
          <rect width="400" height="500" fill="url(#pipeline-glow-1)" />
          <rect width="400" height="500" fill="url(#pipeline-glow-2)" />

          {/* Flowing data streams converging into a central column */}
          <g filter="url(#glow)">
            {/* Left stream */}
            <path
              d="M 60 80 Q 100 140, 140 200 Q 160 240, 180 300 L 190 400"
              stroke="url(#stream-1)"
              strokeWidth="16"
              strokeLinecap="round"
              fill="none"
              opacity="0.8"
            />
            <path
              d="M 60 80 Q 100 140, 140 200 Q 160 240, 180 300 L 190 400"
              stroke="url(#stream-1)"
              strokeWidth="6"
              strokeLinecap="round"
              fill="none"
              opacity="0.9"
            />

            {/* Right stream */}
            <path
              d="M 340 60 Q 300 120, 260 180 Q 230 220, 210 280 L 200 400"
              stroke="url(#stream-2)"
              strokeWidth="14"
              strokeLinecap="round"
              fill="none"
              opacity="0.7"
            />
            <path
              d="M 340 60 Q 300 120, 260 180 Q 230 220, 210 280 L 200 400"
              stroke="url(#stream-2)"
              strokeWidth="5"
              strokeLinecap="round"
              fill="none"
              opacity="0.9"
            />

            {/* Center stream (shortest) */}
            <path
              d="M 200 100 L 195 400"
              stroke="url(#stream-3)"
              strokeWidth="20"
              strokeLinecap="round"
              fill="none"
              opacity="0.6"
            />
            <path
              d="M 200 100 L 195 400"
              stroke="url(#stream-3)"
              strokeWidth="8"
              strokeLinecap="round"
              fill="none"
              opacity="0.95"
            />

            {/* Data nodes along streams */}
            <circle cx="60" cy="80" r="8" fill="#5ce1b5" opacity="0.9" />
            <circle cx="140" cy="200" r="6" fill="#8de8ca" opacity="0.8" />
            <circle cx="340" cy="60" r="7" fill="#8de8ca" opacity="0.85" />
            <circle cx="260" cy="180" r="5" fill="#5ce1b5" opacity="0.75" />
            <circle cx="200" cy="100" r="9" fill="#5ce1b5" opacity="0.95" />
          </g>

          {/* Central column (the pipeline output) */}
          <g filter="url(#glow)">
            <rect
              x="175"
              y="380"
              width="45"
              height="100"
              rx="8"
              fill="url(#stream-3)"
              opacity="0.9"
            />
            <rect
              x="180"
              y="385"
              width="35"
              height="90"
              rx="6"
              fill="#5ce1b5"
              opacity="0.3"
            />
          </g>

          {/* Grain overlay */}
          <rect width="400" height="500" fill="black" opacity="0.03" filter="url(#noise)" />

          {/* Vignette */}
          <rect
            width="400"
            height="500"
            fill="url(#pipeline-glow-2)"
            style={{ mixBlendMode: "multiply" }}
            opacity="0.5"
          />
        </svg>

        <div className="absolute inset-0 bg-gradient-to-t from-[#0a0d12]/90 via-transparent to-transparent" />
      </div>

      {/* Floating Week 1 card */}
      <div className="absolute -bottom-6 -left-2 w-[17rem] -rotate-3 sm:-left-8 sm:w-[19rem] rounded-2xl border border-white/10 bg-card/95 p-4 shadow-xl backdrop-blur">
        <div className="kicker text-mint">Week 1 · complete</div>
        <div className="mt-2 font-display text-xl font-semibold">Introduction &amp; Prerequisites</div>
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
