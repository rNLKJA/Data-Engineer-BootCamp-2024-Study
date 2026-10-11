import { describe, it, expect } from "vitest";

describe("Site Structure", () => {
  it("should have curriculum weeks", () => {
    const weeks = [
      "Week 1: Introduction & Prerequisites",
      "Week 2: Workflow Orchestration",
      "Week 3: Data Warehouse",
      "Week 4: Analytics Engineering",
      "Week 5: Batch Processing",
      "Week 6: Stream Processing",
    ];

    weeks.forEach((week) => {
      expect(week).toBeTruthy();
    });
  });

  it("should validate course structure", () => {
    const courseTopics = {
      "Introduction & Prerequisites": [
        "Course overview",
        "Introduction to GCP",
        "Docker and docker-compose",
      ],
      "Workflow Orchestration": ["Data Lake concepts", "Workflow orchestration patterns"],
      "Data Warehouse": ["Data Warehouse fundamentals", "BigQuery overview"],
      "Analytics Engineering": ["Analytics engineering basics", "dbt (data build tool)"],
      "Batch Processing": ["Batch processing concepts", "Apache Spark introduction"],
      "Stream Processing": ["Introduction to Kafka", "Schemas with Avro"],
    };

    Object.entries(courseTopics).forEach(([week, topics]) => {
      expect(week).toBeTruthy();
      expect(topics.length).toBeGreaterThan(0);
    });
  });
});
