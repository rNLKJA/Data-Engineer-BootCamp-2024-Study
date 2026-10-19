// Screenshot the /project dashboard for the README.
// Uses the Playwright package already installed in web/ and the local Chrome
// (channel: "chrome"), like web/scripts/record-tour.mjs, so nothing is downloaded.
//
//   node scripts/capture_dashboard.mjs [url] [output]
//   node scripts/capture_dashboard.mjs http://localhost:3832/project images/dashboard.png
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const webDir = path.resolve(here, "../../../web");
const require = createRequire(path.join(webDir, "package.json"));
const { chromium } = require("playwright");

const url = process.argv[2] || "http://localhost:3832/project";
const out = path.resolve(process.cwd(), process.argv[3] || "images/dashboard.png");

const browser = await chromium.launch({ channel: "chrome" });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForSelector('svg[aria-label^="Monthly fatal"]');
  await page.waitForTimeout(500); // let the charts settle at the measured width
  // From the top of the page to the end of tile 2 (the two required tiles).
  const bottom = await page.evaluate(() => {
    const tile = document.getElementById("monthly-title")?.closest("section");
    return tile ? Math.ceil(tile.getBoundingClientRect().bottom + window.scrollY + 32) : 2400;
  });
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1280, height: bottom }, fullPage: true });
  console.log(`saved ${out} (1280x${bottom}) from ${url}`);
} finally {
  await browser.close();
}
