import { describe, expect, it } from "vitest";

import data from "../app/project/dashboard-data.json";
import { longDate, monthLabel, niceTicks } from "../app/project/format";

describe("course project dashboard data", () => {
  it("has the two required tiles plus the annual tile", () => {
    expect(data.tiles.crash_type_fsi).toHaveLength(13);
    expect(data.tiles.monthly_fsi).toHaveLength(168);
    expect(data.tiles.annual_people).toHaveLength(14);
  });

  it("covers January 2012 to December 2025 without gaps", () => {
    const months = data.tiles.monthly_fsi.map((r) => r.month);
    expect(months[0]).toBe("2012-01");
    expect(months[months.length - 1]).toBe("2025-12");
    for (let i = 1; i < months.length; i++) {
      const [y0, m0] = months[i - 1].split("-").map(Number);
      const [y1, m1] = months[i].split("-").map(Number);
      expect(y1 * 12 + m1 - (y0 * 12 + m0)).toBe(1);
    }
  });

  it("reconciles every tile with the KPI totals", () => {
    const sum = (rows: { fsi_crashes: number }[]) => rows.reduce((t, r) => t + r.fsi_crashes, 0);
    expect(sum(data.tiles.monthly_fsi)).toBe(data.kpis.fsi_crashes);
    expect(sum(data.tiles.crash_type_fsi)).toBe(data.kpis.fsi_crashes);
    expect(sum(data.tiles.annual_people)).toBe(data.kpis.fsi_crashes);
    expect(data.tiles.annual_people.reduce((t, r) => t + r.fatalities, 0)).toBe(
      data.kpis.fatalities
    );
  });

  it("sorts crash types by FSI crashes and splits them into fatal and serious", () => {
    const rows = data.tiles.crash_type_fsi;
    rows.forEach((r, i) => {
      expect(r.fatal_crashes + r.serious_injury_crashes).toBe(r.fsi_crashes);
      if (i > 0) expect(r.fsi_crashes).toBeLessThanOrEqual(rows[i - 1].fsi_crashes);
    });
  });

  it("ranks only councils and lists the rest separately", () => {
    const top = data.tiles.top_lgas;
    expect(top.map((r) => r.rank)).toEqual(top.map((_, i) => i + 1));
    expect(top.some((r) => r.lga_name.includes("UNINCORP"))).toBe(false);
    const unknown = data.tiles.non_council_lgas.filter((r) => r.is_unknown);
    expect(unknown.map((r) => r.lga_name)).toEqual(["UNINCORPORATED OR UNKNOWN"]);
    expect(unknown[0].crashes).toBe(data.kpis.crashes_without_lga);
  });

  it("flags only the latest year as provisional", () => {
    const flagged = data.tiles.annual_people.filter((r) => r.provisional).map((r) => r.year);
    expect(flagged).toEqual([data.coverage.provisional_year]);
  });

  it("carries the licence and attribution", () => {
    expect(data.source.licence).toBe("CC BY 4.0");
    expect(data.source.attribution).toContain("Department for Infrastructure and Transport");
    expect(data.source.releases.length).toBe(10);
  });
});

describe("format helpers", () => {
  it("formats months and dates without Date objects", () => {
    expect(monthLabel("2024-03")).toBe("Mar 2024");
    expect(longDate("2026-10-09")).toBe("9 October 2026");
  });

  it("makes round ticks from zero", () => {
    expect(niceTicks(96, 4)).toEqual([0, 25, 50, 75, 100]);
    expect(niceTicks(2674, 5)).toEqual([0, 1000, 2000, 3000]);
  });
});
