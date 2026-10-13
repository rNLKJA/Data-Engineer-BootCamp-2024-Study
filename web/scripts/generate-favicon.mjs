#!/usr/bin/env node
import { readFileSync, writeFileSync } from "fs";
import sharp from "sharp";

// Simple pipeline icon in the site's palette
const svg = `<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <rect width="512" height="512" fill="#0a0d12"/>
  <defs>
    <linearGradient id="stream" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5ce1b5" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0d7377" stop-opacity="0.7"/>
    </linearGradient>
  </defs>
  <!-- Three converging streams -->
  <path d="M 128 120 Q 180 200, 220 280 L 240 420" stroke="url(#stream)" stroke-width="32" stroke-linecap="round" fill="none" opacity="0.7"/>
  <path d="M 256 100 L 256 420" stroke="url(#stream)" stroke-width="40" stroke-linecap="round" fill="none" opacity="0.85"/>
  <path d="M 384 120 Q 332 200, 292 280 L 272 420" stroke="url(#stream)" stroke-width="32" stroke-linecap="round" fill="none" opacity="0.7"/>
  <!-- Nodes -->
  <circle cx="128" cy="120" r="18" fill="#5ce1b5" opacity="0.95"/>
  <circle cx="256" cy="100" r="22" fill="#5ce1b5"/>
  <circle cx="384" cy="120" r="18" fill="#5ce1b5" opacity="0.95"/>
</svg>`;

const sizes = [16, 32, 48];

for (const size of sizes) {
  await sharp(Buffer.from(svg)).resize(size, size).png().toFile(`app/favicon-${size}.png`);
}

// Generate ICO (multi-resolution)
const ico16 = await sharp(Buffer.from(svg)).resize(16, 16).png().toBuffer();
const ico32 = await sharp(Buffer.from(svg)).resize(32, 32).png().toBuffer();
const ico48 = await sharp(Buffer.from(svg)).resize(48, 48).png().toBuffer();

writeFileSync("app/favicon.ico", Buffer.concat([ico16, ico32, ico48]));

console.log("✓ Generated favicon");
