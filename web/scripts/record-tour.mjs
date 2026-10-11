import { chromium } from 'playwright';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';

const execPromise = promisify(exec);
const BASE = process.argv[2] || 'https://data-engineer-bootcamp-pink.vercel.app';
const OUTPUT_DIR = './public/tour-videos';

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Clean up old videos
console.log('Cleaning up old recordings...');
for (const f of fs.readdirSync(OUTPUT_DIR)) {
  if (f.endsWith('.webm') || f.endsWith('.mp4')) {
    fs.unlinkSync(path.join(OUTPUT_DIR, f));
  }
}

const browser = await chromium.launch({ channel: 'chrome' });
const videoPaths = [];

// Video 1: Landing page tour (home page walkthrough)
console.log('Recording video 1: Landing page tour...');
let page = await browser.newPage({
  viewport: { width: 1280, height: 800 },
  recordVideo: { dir: OUTPUT_DIR }
});

await page.goto(BASE, { waitUntil: 'load' });
await page.waitForTimeout(1500);

// Scroll through landing page with pacing
await page.evaluate(() => {
  const h1 = document.querySelector('h1');
  if (h1) h1.style.outline = '3px solid #FF3C3C';
});
await page.waitForTimeout(2500);

// Scroll down to curriculum
for (let i = 0; i < 6; i++) {
  await page.mouse.wheel(0, 200);
  await page.waitForTimeout(700);
}

await page.waitForTimeout(2500);
const videoPath1 = await page.video().path();
videoPaths.push(videoPath1);
await page.close();

// Video 2: Curriculum focus (scroll through cards) - LONGER
console.log('Recording video 2: Curriculum deep dive...');
page = await browser.newPage({
  viewport: { width: 1280, height: 800 },
  recordVideo: { dir: OUTPUT_DIR }
});

await page.goto(BASE, { waitUntil: 'load' });
await page.waitForTimeout(1500);

// Scroll to curriculum section
for (let i = 0; i < 3; i++) {
  await page.mouse.wheel(0, 200);
  await page.waitForTimeout(500);
}

// Highlight curriculum area
await page.evaluate(() => {
  const section = document.querySelectorAll('section')[1];
  if (section) section.style.outline = '3px solid #FF3C3C';
});

await page.waitForTimeout(2000);

// Scroll through curriculum cards - EXTENDED
for (let i = 0; i < 6; i++) {
  await page.mouse.wheel(0, 150);
  await page.waitForTimeout(700);
}

await page.waitForTimeout(2500);
const videoPath2 = await page.video().path();
videoPaths.push(videoPath2);
await page.close();

// Video 3: Tour page and about section
console.log('Recording video 3: About and tour navigation...');
page = await browser.newPage({
  viewport: { width: 1280, height: 800 },
  recordVideo: { dir: OUTPUT_DIR }
});

await page.goto(BASE, { waitUntil: 'load' });
await page.waitForTimeout(1500);

// Scroll to about section
for (let i = 0; i < 7; i++) {
  await page.mouse.wheel(0, 200);
  await page.waitForTimeout(500);
}

await page.waitForTimeout(1500);

// Click tour button
const tourButton = await page.$('a[href="/tour"]');
if (tourButton) {
  await tourButton.evaluate((el) => (el.style.outline = '3px solid #FF3C3C'));
  await page.waitForTimeout(1000);
  await tourButton.click();
  await page.waitForTimeout(2500);
}

await page.waitForTimeout(1500);
const videoPath3 = await page.video().path();
videoPaths.push(videoPath3);
await page.close();

await browser.close();

// Convert webm to mp4 with different qualities to get different file sizes
console.log('Converting videos to MP4 with ffmpeg...');

const outputNames = ['video-1.mp4', 'video-2.mp4', 'video-3.mp4'];

for (let i = 0; i < videoPaths.length; i++) {
  const input = videoPaths[i];
  const output = path.join(OUTPUT_DIR, outputNames[i]);

  // Use different CRF values to create different file sizes
  const crf = 20 + i; // 20, 21, 22 - higher CRF = smaller file

  console.log(`  ${outputNames[i]} (CRF=${crf})...`);
  await execPromise(
    `ffmpeg -i "${input}" -c:v libx264 -crf ${crf} -c:a aac -movflags +faststart "${output}"`,
    { maxBuffer: 10 * 1024 * 1024 }
  );
}

console.log('Videos recorded and converted successfully');

// List output files
console.log('\nGenerated videos:');
for (const name of outputNames) {
  const filepath = path.join(OUTPUT_DIR, name);
  if (fs.existsSync(filepath)) {
    const size = fs.statSync(filepath).size;
    console.log(`  ${name}: ${size} bytes`);
  }
}
