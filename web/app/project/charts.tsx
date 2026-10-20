"use client";

// SVG charts for the course project dashboard. The data arrives as props from
// the server page (read from dashboard-data.json); this client island only adds
// width measurement and the hover/focus tooltips. Colours were checked with the
// dataviz palette validator against the card surface (#2f3140): fatal orange and
// serious-injury blue pass every categorical check; the monthly gray is a
// de-emphasis colour, so every value is also in the table under each chart.

import {
  useEffect,
  useRef,
  useState,
  type KeyboardEvent,
  type PointerEvent,
  type ReactNode,
} from "react";

import { COLOURS, monthLabel, nf, niceTicks } from "./format";

function useWidth(initial: number) {
  const ref = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(initial);
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const observer = new ResizeObserver((entries) => {
      const next = Math.round(entries[0]?.contentRect.width ?? 0);
      if (next > 0) setWidth(next);
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  return [ref, width] as const;
}

/** Rectangle with a 4px rounded data-end on the right (horizontal bars). */
function rightRoundedBar(x: number, y: number, w: number, h: number, r = 4): string {
  const rr = Math.max(0, Math.min(r, w / 2, h / 2));
  return `M${x},${y}h${w - rr}a${rr},${rr} 0 0 1 ${rr},${rr}v${h - 2 * rr}a${rr},${rr} 0 0 1 ${-rr},${rr}h${-(w - rr)}z`;
}

/** Rectangle with a 4px rounded data-end on top (columns). */
function topRoundedBar(x: number, y: number, w: number, h: number, r = 4): string {
  const rr = Math.max(0, Math.min(r, w / 2, h));
  return `M${x},${y + h}v${-(h - rr)}a${rr},${rr} 0 0 1 ${rr},${-rr}h${w - 2 * rr}a${rr},${rr} 0 0 1 ${rr},${rr}v${h - rr}z`;
}

type TooltipRow = { key: string; colour?: string; line?: boolean; label: string; value: string };

function Tooltip({
  x,
  y,
  width,
  title,
  rows,
  note,
}: {
  x: number;
  y: number;
  width: number;
  title: string;
  rows: TooltipRow[];
  note?: string;
}) {
  const flip = x > width / 2;
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none absolute z-10 w-56 rounded-xl border border-white/10 bg-[#1e1f29]/95 px-3 py-2.5 text-xs shadow-lg backdrop-blur"
      style={{ top: Math.max(0, y), ...(flip ? { right: width - x + 12 } : { left: x + 12 }) }}
    >
      <p className="font-medium text-muted-foreground">{title}</p>
      <dl className="mt-1.5 space-y-1">
        {rows.map((row) => (
          <div key={row.key} className="flex items-center gap-2">
            {row.colour && (
              <span
                className={
                  row.line ? "h-0.5 w-3 shrink-0 rounded-full" : "size-2 shrink-0 rounded-sm"
                }
                style={{ backgroundColor: row.colour }}
              />
            )}
            <dt className="text-muted-foreground">{row.label}</dt>
            <dd className="ml-auto font-semibold text-foreground tabular-nums">{row.value}</dd>
          </div>
        ))}
      </dl>
      {note && <p className="mt-1.5 text-muted-foreground">{note}</p>}
    </div>
  );
}

export function Legend({
  items,
}: {
  items: { label: string; colour: string; kind: "bar" | "line" }[];
}) {
  return (
    <ul className="flex flex-wrap gap-x-5 gap-y-2 text-sm text-muted-foreground">
      {items.map((item) => (
        <li key={item.label} className="flex items-center gap-2">
          <span
            aria-hidden="true"
            className={item.kind === "line" ? "h-0.5 w-4 rounded-full" : "size-3 rounded-[3px]"}
            style={{ backgroundColor: item.colour }}
          />
          {item.label}
        </li>
      ))}
    </ul>
  );
}

// ---------------------------------------------------------------------------
// Tile 1: FSI crashes by crash type (horizontal stacked bars)
// ---------------------------------------------------------------------------

export type CrashTypeRow = {
  crash_type: string;
  fatal_crashes: number;
  serious_injury_crashes: number;
  fsi_crashes: number;
  fsi_pct_of_casualty_crashes: number;
  fatal_pct_of_fsi: number;
};

export function CrashTypeChart({ rows }: { rows: CrashTypeRow[] }) {
  const [ref, width] = useWidth(720);
  const [active, setActive] = useState<number | null>(null);
  const narrow = width < 560;
  const labelW = narrow ? 0 : Math.min(200, Math.round(width * 0.3));
  const valueW = 52;
  const rowH = narrow ? 44 : 30;
  const barH = 16;
  const top = 22;
  const plotW = Math.max(120, width - labelW - valueW - 8);
  const max = Math.max(...rows.map((r) => r.fsi_crashes));
  const ticks = niceTicks(max, narrow ? 3 : 5);
  const domain = ticks[ticks.length - 1];
  const scale = (v: number) => (v / domain) * plotW;
  const height = top + rows.length * rowH + 4;
  const gap = 2;

  const current = active === null ? null : rows[active];
  const tipY = active === null ? 0 : top + active * rowH + (narrow ? 18 : 0);
  const tipX = current ? labelW + scale(current.fsi_crashes) : 0;

  return (
    <div ref={ref} className="relative w-full min-w-0">
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        role="group"
        aria-label="Fatal and serious injury crashes by crash type, South Australia 2012 to 2025"
        onPointerLeave={() => setActive(null)}
        className="block h-auto max-w-full overflow-visible"
      >
        {ticks.map((t) => (
          <g key={t}>
            <line
              x1={labelW + scale(t)}
              x2={labelW + scale(t)}
              y1={top - 6}
              y2={height}
              stroke={COLOURS.grid}
            />
            <text
              x={labelW + scale(t)}
              y={top - 10}
              textAnchor="middle"
              fontSize={11}
              fill={COLOURS.tick}
              className="tabular-nums"
            >
              {nf.format(t)}
            </text>
          </g>
        ))}
        {rows.map((row, i) => {
          const y = top + i * rowH + (narrow ? 18 : (rowH - barH) / 2);
          const fatalW = scale(row.fatal_crashes);
          const seriousW = scale(row.serious_injury_crashes);
          const dim = active !== null && active !== i;
          return (
            <g
              key={row.crash_type}
              tabIndex={0}
              role="img"
              aria-label={`${row.crash_type}: ${nf.format(row.fsi_crashes)} fatal or serious injury crashes (${nf.format(row.fatal_crashes)} fatal, ${nf.format(row.serious_injury_crashes)} serious injury)`}
              onPointerEnter={() => setActive(i)}
              onFocus={() => setActive(i)}
              onBlur={() => setActive(null)}
              className="outline-none focus-visible:[&>rect.hit]:stroke-[#5ce1b5]"
              opacity={dim ? 0.55 : 1}
            >
              <rect
                className="hit"
                x={0}
                y={top + i * rowH}
                width={width}
                height={rowH}
                fill="transparent"
                strokeWidth={1}
                rx={6}
              />
              <text
                x={narrow ? 0 : labelW - 10}
                y={narrow ? top + i * rowH + 12 : y + barH / 2 + 4}
                textAnchor={narrow ? "start" : "end"}
                fontSize={12.5}
                fill="#f8f8f2"
              >
                {row.crash_type}
              </text>
              <rect
                x={labelW}
                y={y}
                width={Math.max(0, fatalW)}
                height={barH}
                fill={COLOURS.fatal}
              />
              <path
                d={rightRoundedBar(labelW + fatalW + gap, y, Math.max(0, seriousW - gap), barH)}
                fill={COLOURS.serious}
              />
              <text
                x={labelW + fatalW + seriousW + 6}
                y={y + barH / 2 + 4}
                fontSize={12}
                fill="#f8f8f2"
                className="tabular-nums"
              >
                {nf.format(row.fsi_crashes)}
              </text>
            </g>
          );
        })}
        <line x1={labelW} x2={labelW} y1={top - 6} y2={height} stroke={COLOURS.axis} />
      </svg>
      {current && (
        <Tooltip
          x={Math.min(tipX, width - 20)}
          y={tipY}
          width={width}
          title={current.crash_type}
          rows={[
            { key: "fsi", label: "Fatal or serious", value: nf.format(current.fsi_crashes) },
            {
              key: "fatal",
              colour: COLOURS.fatal,
              label: "Fatal",
              value: nf.format(current.fatal_crashes),
            },
            {
              key: "serious",
              colour: COLOURS.serious,
              label: "Serious injury",
              value: nf.format(current.serious_injury_crashes),
            },
          ]}
          note={`${current.fsi_pct_of_casualty_crashes}% of this type's casualty crashes were fatal or serious.`}
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Tile 2: monthly FSI crashes with a 12-month rolling mean
// ---------------------------------------------------------------------------

export type MonthlyRow = {
  month: string;
  fatal_crashes: number;
  serious_injury_crashes: number;
  fsi_crashes: number;
  fsi_rolling_12_mean: number | null;
  provisional: boolean;
};

export type Marker = { month: string; label: string };

export function MonthlyChart({ rows, markers }: { rows: MonthlyRow[]; markers: Marker[] }) {
  const [ref, width] = useWidth(720);
  const [active, setActive] = useState<number | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const narrow = width < 560;
  const left = 36;
  const right = 8;
  const top = 34;
  const bottom = 26;
  const height = narrow ? 260 : 320;
  const plotW = Math.max(100, width - left - right);
  const plotH = height - top - bottom;
  const step = plotW / rows.length;
  const max = Math.max(...rows.map((r) => r.fsi_crashes));
  const ticks = niceTicks(max, 4);
  const domain = ticks[ticks.length - 1];
  const y = (v: number) => top + plotH - (v / domain) * plotH;
  const xCentre = (i: number) => left + step * i + step / 2;
  const barW = Math.max(1, step - 2);
  const index = (month: string) => rows.findIndex((r) => r.month === month);

  const linePoints = rows
    .map((r, i) =>
      r.fsi_rolling_12_mean === null
        ? null
        : `${xCentre(i).toFixed(1)},${y(r.fsi_rolling_12_mean).toFixed(1)}`
    )
    .filter((p): p is string => p !== null);

  const provisionalStart = rows.findIndex((r) => r.provisional);
  const years = rows
    .map((r, i) => ({ i, year: r.month.slice(0, 4), jan: r.month.endsWith("-01") }))
    .filter((r) => r.jan);
  const yearEvery = narrow ? 3 : width < 760 ? 2 : 1;

  // Markers closer than three months share one label (Dec 2016 and Jan 2017).
  const markerGroups: { indices: number[]; label: string }[] = [];
  for (const marker of markers) {
    const i = index(marker.month);
    if (i < 0) continue;
    const last = markerGroups[markerGroups.length - 1];
    if (last && i - last.indices[last.indices.length - 1] <= 3) last.indices.push(i);
    else markerGroups.push({ indices: [i], label: marker.label });
  }

  function pick(clientX: number) {
    const box = svgRef.current?.getBoundingClientRect();
    if (!box) return;
    const i = Math.floor((clientX - box.left - left) / step);
    setActive(Math.max(0, Math.min(rows.length - 1, i)));
  }

  function onKey(event: KeyboardEvent<SVGSVGElement>) {
    const moves: Record<string, (i: number) => number> = {
      ArrowLeft: (i) => i - 1,
      ArrowRight: (i) => i + 1,
      Home: () => 0,
      End: () => rows.length - 1,
      PageUp: (i) => i - 12,
      PageDown: (i) => i + 12,
    };
    const move = moves[event.key];
    if (!move) return;
    event.preventDefault();
    setActive((current) =>
      Math.max(0, Math.min(rows.length - 1, move(current ?? rows.length - 1)))
    );
  }

  const current = active === null ? null : rows[active];

  return (
    <div ref={ref} className="relative w-full min-w-0">
      <svg
        ref={svgRef}
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        tabIndex={0}
        aria-label="Monthly fatal and serious injury crashes in South Australia, January 2012 to December 2025, with a 12-month rolling mean. Use the arrow keys to read each month."
        onPointerMove={(event: PointerEvent<SVGSVGElement>) => pick(event.clientX)}
        onPointerLeave={() => setActive(null)}
        onKeyDown={onKey}
        onBlur={() => setActive(null)}
        className="block h-auto max-w-full rounded-md outline-none focus-visible:ring-2 focus-visible:ring-mint/70"
      >
        {provisionalStart >= 0 && (
          <g>
            <rect
              x={left + step * provisionalStart}
              y={top}
              width={step * (rows.length - provisionalStart)}
              height={plotH}
              fill={COLOURS.provisional}
            />
            <text x={left + plotW} y={top - 8} textAnchor="end" fontSize={11} fill={COLOURS.tick}>
              {rows[provisionalStart].month.slice(0, 4)} provisional
            </text>
          </g>
        )}
        {ticks.map((t) => (
          <g key={t}>
            <line
              x1={left}
              x2={left + plotW}
              y1={y(t)}
              y2={y(t)}
              stroke={t === 0 ? COLOURS.axis : COLOURS.grid}
            />
            <text
              x={left - 8}
              y={y(t) + 4}
              textAnchor="end"
              fontSize={11}
              fill={COLOURS.tick}
              className="tabular-nums"
            >
              {nf.format(t)}
            </text>
          </g>
        ))}
        {markerGroups.map((group) => {
          const x0 = left + step * group.indices[0];
          return (
            <g key={group.indices.join("-")}>
              {group.indices.map((i) => (
                <line
                  key={i}
                  x1={left + step * i}
                  x2={left + step * i}
                  y1={top - 4}
                  y2={top + plotH}
                  stroke={COLOURS.marker}
                />
              ))}
              <text x={x0 + 4} y={top + 10} fontSize={10.5} fill={COLOURS.tick}>
                {narrow ? "PDO" : group.label}
              </text>
            </g>
          );
        })}
        {rows.map((r, i) => (
          <rect
            key={r.month}
            x={left + step * i + (step - barW) / 2}
            y={y(r.fsi_crashes)}
            width={barW}
            height={top + plotH - y(r.fsi_crashes)}
            fill={active === i ? "#9a9eb3" : COLOURS.monthly}
          />
        ))}
        <polyline
          points={linePoints.join(" ")}
          fill="none"
          stroke={COLOURS.accent}
          strokeWidth={2}
          strokeLinejoin="round"
          strokeLinecap="round"
        />
        {years.map(({ i, year }, n) =>
          n % yearEvery === 0 ? (
            <text
              key={year}
              x={left + step * i + 1}
              y={height - 8}
              fontSize={11}
              fill={COLOURS.tick}
              className="tabular-nums"
            >
              {year}
            </text>
          ) : null
        )}
        {current && active !== null && (
          <g pointerEvents="none">
            <line
              x1={xCentre(active)}
              x2={xCentre(active)}
              y1={top}
              y2={top + plotH}
              stroke="#f8f8f2"
              strokeOpacity={0.5}
            />
            {current.fsi_rolling_12_mean !== null && (
              <circle
                cx={xCentre(active)}
                cy={y(current.fsi_rolling_12_mean)}
                r={4}
                fill={COLOURS.accent}
                stroke={COLOURS.surface}
                strokeWidth={2}
              />
            )}
          </g>
        )}
      </svg>
      {current && active !== null && (
        <Tooltip
          x={xCentre(active)}
          y={top}
          width={width}
          title={`${monthLabel(current.month)}${current.provisional ? " (provisional)" : ""}`}
          rows={[
            {
              key: "fsi",
              colour: COLOURS.monthly,
              label: "Fatal or serious",
              value: nf.format(current.fsi_crashes),
            },
            { key: "fatal", label: "Fatal", value: nf.format(current.fatal_crashes) },
            {
              key: "serious",
              label: "Serious injury",
              value: nf.format(current.serious_injury_crashes),
            },
            {
              key: "mean",
              colour: COLOURS.accent,
              line: true,
              label: "12-month mean",
              value:
                current.fsi_rolling_12_mean === null
                  ? "n/a"
                  : current.fsi_rolling_12_mean.toFixed(1),
            },
          ]}
        />
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Tile 3: people killed and admitted to hospital per year (small multiples)
// ---------------------------------------------------------------------------

export type AnnualRow = {
  year: number;
  fatalities: number;
  admitted_to_hospital: number;
  provisional: boolean;
};

function AnnualColumns({
  rows,
  field,
  colour,
  title,
}: {
  rows: AnnualRow[];
  field: "fatalities" | "admitted_to_hospital";
  colour: string;
  title: string;
}) {
  const [ref, width] = useWidth(340);
  const [active, setActive] = useState<number | null>(null);
  const left = 34;
  const top = 22;
  const bottom = 24;
  const height = 210;
  const plotW = Math.max(100, width - left - 4);
  const plotH = height - top - bottom;
  const values = rows.map((r) => r[field]);
  const ticks = niceTicks(Math.max(...values), 3);
  const domain = ticks[ticks.length - 1];
  const step = plotW / rows.length;
  const barW = Math.min(24, step - 2);
  const y = (v: number) => top + plotH - (v / domain) * plotH;
  const maxIndex = values.indexOf(Math.max(...values));
  const lastIndex = rows.length - 1;
  const current = active === null ? null : rows[active];

  return (
    <figure className="min-w-0">
      <figcaption className="text-sm font-semibold text-foreground">{title}</figcaption>
      <div ref={ref} className="relative mt-2 w-full min-w-0">
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          role="group"
          aria-label={`${title} per year, ${rows[0].year} to ${rows[lastIndex].year}`}
          onPointerLeave={() => setActive(null)}
          className="block h-auto max-w-full overflow-visible"
        >
          {ticks.map((t) => (
            <g key={t}>
              <line
                x1={left}
                x2={left + plotW}
                y1={y(t)}
                y2={y(t)}
                stroke={t === 0 ? COLOURS.axis : COLOURS.grid}
              />
              <text
                x={left - 6}
                y={y(t) + 4}
                textAnchor="end"
                fontSize={11}
                fill={COLOURS.tick}
                className="tabular-nums"
              >
                {nf.format(t)}
              </text>
            </g>
          ))}
          {rows.map((r, i) => {
            const value = r[field];
            const x = left + step * i + (step - barW) / 2;
            const labelled = i === maxIndex || i === lastIndex;
            return (
              <g
                key={r.year}
                tabIndex={0}
                role="img"
                aria-label={`${r.year}${r.provisional ? " (provisional)" : ""}: ${nf.format(value)}`}
                onPointerEnter={() => setActive(i)}
                onFocus={() => setActive(i)}
                onBlur={() => setActive(null)}
                className="outline-none"
              >
                <rect x={left + step * i} y={top} width={step} height={plotH} fill="transparent" />
                <path
                  d={topRoundedBar(x, y(value), barW, top + plotH - y(value))}
                  fill={colour}
                  fillOpacity={r.provisional ? 0.45 : active === null || active === i ? 1 : 0.6}
                />
                {labelled && (
                  <text
                    x={x + barW / 2}
                    y={y(value) - 5}
                    textAnchor="middle"
                    fontSize={11}
                    fill="#f8f8f2"
                    className="tabular-nums"
                  >
                    {nf.format(value)}
                  </text>
                )}
                {((i % 3 === 0 && lastIndex - i >= 3) || i === lastIndex) && (
                  <text
                    x={x + barW / 2}
                    y={height - 8}
                    textAnchor="middle"
                    fontSize={11}
                    fill={COLOURS.tick}
                    className="tabular-nums"
                  >
                    {`${r.year}${r.provisional ? "*" : ""}`}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
        {current && active !== null && (
          <Tooltip
            x={left + step * active + step / 2}
            y={top}
            width={width}
            title={`${current.year}${current.provisional ? " (provisional)" : ""}`}
            rows={[{ key: field, colour, label: title, value: nf.format(current[field]) }]}
          />
        )}
      </div>
    </figure>
  );
}

export function AnnualChart({ rows }: { rows: AnnualRow[] }): ReactNode {
  return (
    <div className="grid gap-8 md:grid-cols-2">
      <AnnualColumns rows={rows} field="fatalities" colour={COLOURS.fatal} title="Lives lost" />
      <AnnualColumns
        rows={rows}
        field="admitted_to_hospital"
        colour={COLOURS.serious}
        title="People admitted to hospital"
      />
    </div>
  );
}
