// Week 7 course project dashboard: serious road crashes in South Australia.
// Every number on this page is read from ./dashboard-data.json, which
// original/project/pipeline/export_dashboard.py writes from the dbt reporting
// models. CI reruns the pipeline and fails if the committed JSON differs.
import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowUpRight } from "lucide-react";

import data from "./dashboard-data.json";
import { AnnualChart, CrashTypeChart, Legend, MonthlyChart, type Marker } from "./charts";
import { COLOURS, longDate, monthLabel, nf, yearSpan } from "./format";

const REPO = "https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study";
const PROJECT_README = `${REPO}/tree/main/original/project#readme`;

export const metadata: Metadata = {
  title: "Course project: serious road crashes in South Australia",
  description:
    "Week 7 course project: a batch pipeline (Prefect, Parquet lake, dbt on DuckDB) over South Australia's road crash data, 2012 to 2025, with a two-tile dashboard.",
};

const { kpis, coverage, source, tiles } = data;
const first = coverage.first_year;
const last = coverage.last_year;
const provisional = coverage.provisional_year;

// Release as-at dates, grouped so each date lists the years it covers.
const releaseGroups = Object.values(
  source.releases.reduce<Record<string, { asAt: string; first: number; last: number }>>(
    (groups, r) => {
      const group = groups[r.as_at] ?? { asAt: r.as_at, first: r.first_year, last: r.last_year };
      group.first = Math.min(group.first, r.first_year);
      group.last = Math.max(group.last, r.last_year);
      groups[r.as_at] = group;
      return groups;
    },
    {}
  )
).sort((a, b) => a.first - b.first);

// PDO reporting rule changes that fall inside the charted months.
const markers: Marker[] = data.pdo_regimes
  .map((regime) => ({ month: regime.valid_from.slice(0, 7), label: "PDO rules changed" }))
  .filter((m) => m.month > coverage.first_month && m.month <= coverage.last_month);

const ruleChanges = data.pdo_regimes
  .filter((r) => r.valid_from.slice(0, 7) > coverage.first_month)
  .map((r) => longDate(r.valid_from));

const topType = tiles.crash_type_fsi[0];
const country = tiles.regions.find((r) => r.stats_area === "Country");

function SourceNote() {
  return (
    <p className="mt-5 text-xs leading-relaxed text-muted-foreground">
      Source:{" "}
      <a href={source.page} className="text-mint underline-offset-4 hover:underline">
        {source.title}
      </a>
      , {source.publisher}, data.sa.gov.au,{" "}
      <a href={source.licence_url} className="text-mint underline-offset-4 hover:underline">
        {source.licence}
      </a>
      . Releases as at{" "}
      {releaseGroups.map((g, i) => (
        <span key={g.asAt}>
          {i > 0 && (i === releaseGroups.length - 1 ? " and " : ", ")}
          {longDate(g.asAt)} ({yearSpan(g.first, g.last)})
        </span>
      ))}
      . {provisional} is provisional: DIT still revises the latest year.
    </p>
  );
}

function Tile({
  id,
  kicker,
  title,
  description,
  children,
}: {
  id: string;
  kicker: string;
  title: string;
  description: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section
      aria-labelledby={`${id}-title`}
      className="min-w-0 rounded-3xl border border-white/10 bg-card p-5 sm:p-8"
    >
      <p className="kicker text-teal">{kicker}</p>
      <h2 id={`${id}-title`} className="mt-2 font-display text-2xl font-semibold sm:text-3xl">
        {title}
      </h2>
      <div className="mt-3 max-w-3xl text-sm leading-relaxed text-muted-foreground">
        {description}
      </div>
      {children}
      <SourceNote />
    </section>
  );
}

function DataTable({
  summary,
  head,
  rows,
}: {
  summary: string;
  head: string[];
  rows: (string | number)[][];
}) {
  return (
    <details className="mt-6 rounded-2xl border border-white/10 bg-background/40 px-4 py-3 text-sm">
      <summary className="cursor-pointer font-medium text-foreground">{summary}</summary>
      <div className="mt-3 max-h-96 overflow-auto">
        <table className="w-full border-collapse text-left">
          <thead className="sticky top-0 bg-card">
            <tr>
              {head.map((h, i) => (
                <th
                  key={h}
                  scope="col"
                  className={`border-b border-white/10 py-2 pr-4 font-medium text-muted-foreground ${i > 0 ? "text-right" : ""}`}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={String(row[0])} className="border-b border-white/5">
                {row.map((cell, i) =>
                  i === 0 ? (
                    <th key={i} scope="row" className="py-1.5 pr-4 font-normal">
                      {cell}
                    </th>
                  ) : (
                    <td key={i} className="py-1.5 pr-4 text-right tabular-nums">
                      {typeof cell === "number" ? nf.format(cell) : cell}
                    </td>
                  )
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}

export default function ProjectPage() {
  const stats = [
    { label: "Crashes reported", value: kpis.crashes, note: `${first} to ${last}, all severities` },
    {
      label: "Casualties",
      value: kpis.casualties,
      note: "People killed or injured",
    },
    { label: "Lives lost", value: kpis.fatalities, note: "Died within 30 days of the crash" },
    {
      label: "Fatal or serious injury crashes",
      value: kpis.fsi_crashes,
      note: `${nf.format(kpis.fatal_crashes)} fatal crashes`,
    },
  ];

  return (
    <div className="dark flex min-h-dvh flex-col">
      <header className="mx-auto w-full max-w-6xl px-4 pt-8 sm:px-6">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-mint"
        >
          <ArrowLeft className="size-4" aria-hidden="true" />
          Back to the curriculum
        </Link>
      </header>

      <main id="main" className="mx-auto w-full max-w-6xl flex-1 px-4 pb-24 sm:px-6">
        <section className="pt-10 pb-12">
          <p className="kicker text-mint">Week 7 · Course project · Complete</p>
          <h1 className="mt-4 max-w-4xl font-display text-4xl leading-[1.05] font-semibold tracking-tight sm:text-5xl lg:text-6xl">
            Serious road crashes in <em className="text-mint not-italic">South Australia</em>,{" "}
            {first} to {last}.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-relaxed text-muted-foreground">
            {data.question} A batch pipeline loads {source.releases.length} public releases from the
            Department for Infrastructure and Transport into a Parquet lake, models them with dbt on
            DuckDB, and exports the numbers on this page. The tiles count fatal or serious injury
            (FSI) crashes because those are recorded the same way in every year.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <a
              href={PROJECT_README}
              className="inline-flex h-11 items-center gap-2 rounded-full bg-mint px-5 text-sm font-semibold text-graphite-deep transition-colors hover:bg-mint/90"
            >
              Project write-up and code
              <ArrowUpRight className="size-4" aria-hidden="true" />
            </a>
            <a
              href={source.page}
              className="inline-flex h-11 items-center gap-2 rounded-full border border-white/10 bg-card px-5 text-sm font-medium transition-colors hover:border-mint/50"
            >
              Dataset on data.sa.gov.au
              <ArrowUpRight className="size-4" aria-hidden="true" />
            </a>
          </div>
        </section>

        <section aria-labelledby="kpi-title">
          <h2 id="kpi-title" className="sr-only">
            Headline numbers
          </h2>
          <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map((s) => (
              <div key={s.label} className="rounded-3xl border border-white/10 bg-card p-6">
                <dt className="text-sm text-muted-foreground">{s.label}</dt>
                <dd className="mt-2 font-display text-4xl font-semibold text-foreground">
                  {nf.format(s.value)}
                </dd>
                <dd className="mt-1 text-xs text-muted-foreground">{s.note}</dd>
              </div>
            ))}
          </dl>
        </section>

        <div className="mt-8 grid min-w-0 gap-8">
          <Tile
            id="crash-types"
            kicker="Tile 1 · How"
            title="Fatal and serious injury crashes by crash type"
            description={
              <p>
                All {tiles.crash_type_fsi.length} DIT crash types, {first} to {last}, sorted by FSI
                crashes. {topType.crash_type} leads with {nf.format(topType.fsi_crashes)} (
                {topType.pct_of_all_fsi}% of all FSI crashes). Hover or tab through the bars for the
                severity mix.
              </p>
            }
          >
            <div className="mt-6">
              <Legend
                items={[
                  { label: "Fatal crash", colour: COLOURS.fatal, kind: "bar" },
                  { label: "Serious injury crash", colour: COLOURS.serious, kind: "bar" },
                ]}
              />
            </div>
            <div className="mt-4">
              <CrashTypeChart rows={tiles.crash_type_fsi} />
            </div>
            <p className="mt-2 text-xs text-muted-foreground">
              Horizontal axis: number of crashes. Label at the end of each bar: fatal plus serious.
            </p>
            <DataTable
              summary="Show the data table"
              head={[
                "Crash type",
                "Fatal",
                "Serious injury",
                "FSI total",
                "All crashes",
                "FSI % of casualty crashes",
              ]}
              rows={tiles.crash_type_fsi.map((r) => [
                r.crash_type,
                r.fatal_crashes,
                r.serious_injury_crashes,
                r.fsi_crashes,
                r.crashes,
                `${r.fsi_pct_of_casualty_crashes}%`,
              ])}
            />
          </Tile>

          <Tile
            id="monthly"
            kicker="Tile 2 · When"
            title="Fatal and serious injury crashes per month"
            description={
              <p>
                {coverage.months} months from {monthLabel(coverage.first_month)} to{" "}
                {monthLabel(coverage.last_month)}. Gray columns are monthly counts; the line is the
                mean of the trailing 12 months. Orange hairlines mark the property-damage-only
                reporting rule changes ({ruleChanges.join(", ")}): they changed how many minor
                crashes were recorded, not FSI crashes, which is why this tile counts FSI. The
                shaded year is provisional.
              </p>
            }
          >
            <div className="mt-6">
              <Legend
                items={[
                  { label: "Monthly FSI crashes", colour: COLOURS.monthly, kind: "bar" },
                  { label: "12-month rolling mean", colour: COLOURS.accent, kind: "line" },
                ]}
              />
            </div>
            <div className="mt-4">
              <MonthlyChart rows={tiles.monthly_fsi} markers={markers} />
            </div>
            <p className="mt-2 text-xs text-muted-foreground">
              Vertical axis: crashes per month. Horizontal axis: month. Use the arrow keys on the
              focused chart to step through months.
            </p>
            <DataTable
              summary="Show the data table (168 months)"
              head={["Month", "Fatal", "Serious injury", "FSI total", "12-month mean"]}
              rows={tiles.monthly_fsi.map((r) => [
                `${monthLabel(r.month)}${r.provisional ? " (provisional)" : ""}`,
                r.fatal_crashes,
                r.serious_injury_crashes,
                r.fsi_crashes,
                r.fsi_rolling_12_mean === null ? "n/a" : r.fsi_rolling_12_mean.toFixed(2),
              ])}
            />
          </Tile>

          <Tile
            id="people"
            kicker="Tile 3 · People"
            title="People killed and admitted to hospital each year"
            description={
              <p>
                Counted from the casualty records: a fatality is a death within 30 days of the
                crash; a serious injury is an admission to hospital. Two separate scales, so two
                charts. {provisional} (marked *) is provisional.
              </p>
            }
          >
            <div className="mt-6">
              <AnnualChart rows={tiles.annual_people} />
            </div>
            <DataTable
              summary="Show the data table"
              head={[
                "Year",
                "Lives lost",
                "Admitted to hospital",
                "Fatal crashes",
                "Serious injury crashes",
              ]}
              rows={tiles.annual_people.map((r) => [
                `${r.year}${r.provisional ? " (provisional)" : ""}`,
                r.fatalities,
                r.admitted_to_hospital,
                r.fatal_crashes,
                r.serious_injury_crashes,
              ])}
            />
          </Tile>

          <section
            aria-labelledby="where-title"
            className="min-w-0 rounded-3xl border border-white/10 bg-card p-5 sm:p-8"
          >
            <p className="kicker text-teal">Supporting question · Where</p>
            <h2 id="where-title" className="mt-2 font-display text-2xl font-semibold sm:text-3xl">
              Regions and council areas
            </h2>
            <p className="mt-3 max-w-3xl text-sm leading-relaxed text-muted-foreground">
              These are counts, not rates: the data has no population or traffic volume. The Country
              area (outside metropolitan Adelaide) accounts for{" "}
              {country ? `${country.pct_of_all_fsi}%` : "a large share"} of FSI crashes, and{" "}
              {country ? `${country.fsi_pct_of_casualty_crashes}%` : "a high share"} of its casualty
              crashes are fatal or serious.
            </p>
            <div className="mt-6 grid gap-8 lg:grid-cols-2">
              <div className="min-w-0">
                <h3 className="font-semibold">By statistical area</h3>
                <div className="mt-3 overflow-x-auto">
                  <table className="w-full border-collapse text-left text-sm">
                    <thead>
                      <tr>
                        {["Area", "FSI crashes", "Share of FSI", "FSI % of casualty crashes"].map(
                          (h, i) => (
                            <th
                              key={h}
                              scope="col"
                              className={`border-b border-white/10 py-2 pr-3 font-medium text-muted-foreground ${i > 0 ? "text-right" : ""}`}
                            >
                              {h}
                            </th>
                          )
                        )}
                      </tr>
                    </thead>
                    <tbody>
                      {tiles.regions.map((r) => (
                        <tr key={r.stats_area} className="border-b border-white/5">
                          <th scope="row" className="py-1.5 pr-3 font-normal">
                            {r.stats_area}
                          </th>
                          <td className="py-1.5 pr-3 text-right tabular-nums">
                            {nf.format(r.fsi_crashes)}
                          </td>
                          <td className="py-1.5 pr-3 text-right tabular-nums">
                            {r.pct_of_all_fsi}%
                          </td>
                          <td className="py-1.5 pr-3 text-right tabular-nums">
                            {r.fsi_pct_of_casualty_crashes}%
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <div className="min-w-0">
                <h3 className="font-semibold">
                  Top {tiles.top_lgas.length} council areas by FSI crashes
                </h3>
                <div className="mt-3 overflow-x-auto">
                  <table className="w-full border-collapse text-left text-sm">
                    <thead>
                      <tr>
                        {["Council area (DIT name)", "FSI", "Fatal"].map((h, i) => (
                          <th
                            key={h}
                            scope="col"
                            className={`border-b border-white/10 py-2 pr-3 font-medium text-muted-foreground ${i > 0 ? "text-right" : ""}`}
                          >
                            {h}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {tiles.top_lgas.map((r) => (
                        <tr key={r.lga_name} className="border-b border-white/5">
                          <th scope="row" className="py-1.5 pr-3 font-normal">
                            {r.lga_name}
                          </th>
                          <td className="py-1.5 pr-3 text-right tabular-nums">
                            {nf.format(r.fsi_crashes)}
                          </td>
                          <td className="py-1.5 pr-3 text-right tabular-nums">
                            {nf.format(r.fatal_crashes)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <p className="mt-2 text-xs text-muted-foreground">
                  {nf.format(kpis.crashes_without_lga)} crashes have no council recorded; they are
                  grouped as UNINCORPORATED OR UNKNOWN.
                </p>
              </div>
            </div>
            <SourceNote />
          </section>

          <section
            aria-labelledby="pipeline-title"
            className="rounded-3xl border border-white/10 bg-gradient-to-br from-graphite-deep/70 to-graphite-deep/40 p-5 sm:p-8"
          >
            <p className="kicker text-mint">How the numbers get here</p>
            <h2
              id="pipeline-title"
              className="mt-2 font-display text-2xl font-semibold sm:text-3xl"
            >
              From data.sa.gov.au to this page
            </h2>
            <ol className="mt-5 grid gap-3 text-sm leading-relaxed text-muted-foreground md:grid-cols-2">
              <li>
                <span className="font-semibold text-foreground">1. Fetch.</span> A Prefect 3 flow
                downloads {source.releases.length} pinned zips, with retries and a SHA-256 check
                against the manifest.
              </li>
              <li>
                <span className="font-semibold text-foreground">2. Validate and land.</span> A
                header contract and row checks, then Hive-partitioned Parquet, one folder per year.
              </li>
              <li>
                <span className="font-semibold text-foreground">3. Transform.</span> dbt on DuckDB
                (standing in for BigQuery) builds staging, core and reporting models, with data
                tests that reconcile casualties and units with the crash totals.
              </li>
              <li>
                <span className="font-semibold text-foreground">4. Export.</span> A deterministic
                JSON file feeds this static page. CI reruns everything and fails if the numbers
                change.
              </li>
            </ol>
          </section>
        </div>
      </main>

      <footer className="border-t border-white/10">
        <div className="mx-auto flex max-w-6xl flex-col items-center gap-3 px-4 py-12 text-center text-sm text-muted-foreground sm:px-6">
          <p>Completed in October 2026 with Claude as a pair programmer.</p>
          <p className="max-w-3xl text-xs">{source.attribution}.</p>
          <p>
            <a
              href="https://rin.contact"
              className="text-mint underline-offset-4 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Made by Rin in Adelaide
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}
