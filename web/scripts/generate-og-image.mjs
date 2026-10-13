#!/usr/bin/env node
import sharp from "sharp";

// OG image with site branding: 1200x630
const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="#0a0d12"/>

  <defs>
    <linearGradient id="stream" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5ce1b5" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0d7377" stop-opacity="0.6"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.3">
      <stop offset="0%" stop-color="#5ce1b5" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#0a0d12" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background glow -->
  <rect width="1200" height="630" fill="url(#glow)"/>

  <!-- Data pipeline streams (abstract) -->
  <g opacity="0.6">
    <path d="M 200 150 Q 350 250, 500 350 L 550 550" stroke="url(#stream)" stroke-width="48" stroke-linecap="round" fill="none"/>
    <path d="M 600 100 L 600 550" stroke="url(#stream)" stroke-width="60" stroke-linecap="round" fill="none"/>
    <path d="M 1000 150 Q 850 250, 700 350 L 650 550" stroke="url(#stream)" stroke-width="48" stroke-linecap="round" fill="none"/>
  </g>

  <!-- Nodes -->
  <circle cx="200" cy="150" r="28" fill="#5ce1b5" opacity="0.9"/>
  <circle cx="600" cy="100" r="36" fill="#5ce1b5"/>
  <circle cx="1000" cy="150" r="28" fill="#5ce1b5" opacity="0.9"/>

  <!-- Text -->
  <text x="600" y="280" font-family="system-ui, -apple-system, sans-serif" font-size="68" font-weight="700" fill="#f8f9f9" text-anchor="middle" letter-spacing="-0.02em">Data Engineer BootCamp</text>
  <text x="600" y="350" font-family="ui-monospace, monospace" font-size="28" fill="#a9adc6" text-anchor="middle" letter-spacing="0.08em" text-transform="uppercase">Six weeks · Hands-on training</text>
</svg>`;

await sharp(Buffer.from(svg)).png().toFile("public/og-image.png");

console.log("✓ Generated OG image");
