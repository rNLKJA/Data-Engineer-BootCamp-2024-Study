// Shared formatting helpers and chart colours for the course project page.
// Plain module (no "use client") so both the server page and the chart island use it.

export const COLOURS = {
  fatal: "#d95926",
  serious: "#3987e5",
  accent: "#5ce1b5",
  monthly: "#666a80",
  surface: "#2f3140",
  grid: "rgba(248, 248, 242, 0.08)",
  axis: "rgba(248, 248, 242, 0.22)",
  tick: "#b4b8cc",
  provisional: "rgba(248, 248, 242, 0.05)",
  marker: "rgba(255, 184, 108, 0.7)",
} as const;

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const MONTHS_LONG = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

export const nf = new Intl.NumberFormat("en-AU");

/** "2024-03" -> "Mar 2024" (no Date objects, so no time-zone surprises). */
export function monthLabel(month: string): string {
  const [year, mm] = month.split("-");
  return `${MONTHS[Number(mm) - 1]} ${year}`;
}

/** "2026-10-09" -> "9 October 2026". */
export function longDate(iso: string): string {
  const [year, mm, dd] = iso.split("-");
  return `${Number(dd)} ${MONTHS_LONG[Number(mm) - 1]} ${year}`;
}

/** Round axis ticks from zero: 0, 25, 50, 75, 100 and so on. */
export function niceTicks(max: number, count = 4): number[] {
  if (max <= 0) return [0];
  const raw = max / count;
  const magnitude = 10 ** Math.floor(Math.log10(raw));
  const norm = raw / magnitude;
  const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 2.5 ? 2.5 : norm <= 5 ? 5 : 10) * magnitude;
  const ticks: number[] = [];
  const top = Math.ceil(max / step) * step;
  for (let v = 0; v <= top + step / 1000; v += step) {
    ticks.push(Math.round(v * 1000) / 1000);
  }
  return ticks;
}

/** "2012" or "2021 to 2025" */
export function yearSpan(first: number, last: number): string {
  return first === last ? String(first) : `${first} to ${last}`;
}
