"use client";

export default function Home() {
  const weeks = [
    {
      week: "Week 1",
      title: "Introduction & Prerequisites",
      status: "complete" as const,
      topics: [
        "Course overview",
        "Introduction to GCP",
        "Docker and docker-compose",
        "Postgres with Docker",
        "Infrastructure with Terraform",
      ],
    },
    {
      week: "Week 2",
      title: "Workflow Orchestration",
      status: "upcoming" as const,
      topics: [
        "Data Lake concepts",
        "Workflow orchestration patterns",
        "Introduction to Prefect",
        "ETL with GCP & Prefect",
        "Parametrizing workflows",
      ],
    },
    {
      week: "Week 3",
      title: "Data Warehouse",
      status: "upcoming" as const,
      topics: [
        "Data Warehouse fundamentals",
        "BigQuery overview",
        "Partitioning and clustering",
        "BigQuery best practices",
        "BigQuery internals",
      ],
    },
    {
      week: "Week 4",
      title: "Analytics Engineering",
      status: "upcoming" as const,
      topics: [
        "Analytics engineering basics",
        "dbt (data build tool)",
        "Models and testing",
        "Cloud and local deployment",
        "Data visualization",
      ],
    },
    {
      week: "Week 5",
      title: "Batch Processing",
      status: "upcoming" as const,
      topics: [
        "Batch processing concepts",
        "Apache Spark introduction",
        "Spark DataFrames",
        "Spark SQL",
        "GroupBy and joins internals",
      ],
    },
    {
      week: "Week 6",
      title: "Stream Processing",
      status: "upcoming" as const,
      topics: [
        "Introduction to Kafka",
        "Schemas with Avro",
        "Kafka Streams",
        "Kafka Connect and KSQL",
        "Real-time data pipelines",
      ],
    },
  ];

  return (
    <div className="flex flex-col bg-background text-foreground">
      {/* Hero */}
      <section className="border-b border-card-border px-6 py-16 sm:px-8 sm:py-24 md:py-32">
        <div className="mx-auto max-w-4xl space-y-8">
          <div className="space-y-4">
            <p className="text-sm font-mono tracking-wider text-teal uppercase">
              Data Engineering Fundamentals
            </p>
            <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-5xl md:text-6xl">
              Data Engineer BootCamp
            </h1>
          </div>
          <p className="max-w-2xl text-lg leading-relaxed text-slate">
            Learn data engineering fundamentals through hands-on lessons spanning orchestration,
            warehousing, analytics, batch and stream processing. Six weeks of practical training
            built on real-world tools and patterns.
          </p>
        </div>
      </section>

      {/* Pipeline Timeline */}
      <section className="px-6 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-6xl">
          <div className="mb-12 flex items-end justify-between">
            <h2 className="text-2xl font-bold leading-tight">Curriculum</h2>
            <p className="text-sm text-slate">6 weeks, scaffolded by stage</p>
          </div>

          {/* Pipeline visual */}
          <div className="space-y-3">
            {weeks.map((item, index) => {
              const isComplete = item.status === "complete";
              const statusColor = isComplete ? "teal" : "slate";
              const bgOpacity = isComplete
                ? "bg-teal/10 dark:bg-teal/5"
                : "bg-graphite/5 dark:bg-graphite/10";
              const borderColor = isComplete
                ? "border-teal/30 dark:border-teal/20"
                : "border-graphite/20 dark:border-graphite/30";
              const textColor = isComplete ? "text-foreground" : "text-slate";

              return (
                <div
                  key={item.week}
                  className={`group relative overflow-hidden rounded-lg border transition-all hover:border-teal/50 ${bgOpacity} ${borderColor}`}
                >
                  {/* Background gradient accent */}
                  {isComplete && (
                    <div className="absolute -right-32 -top-32 h-64 w-64 rounded-full bg-teal/5 blur-3xl" />
                  )}

                  <div className="relative px-6 py-5 sm:flex sm:items-center sm:justify-between">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        {/* Status indicator */}
                        <div
                          className={`h-2 w-2 rounded-full ${
                            isComplete ? "bg-teal" : "bg-graphite"
                          }`}
                        />
                        <span className="text-sm font-mono font-semibold tracking-wider text-teal">
                          {item.week}
                        </span>
                        {isComplete && (
                          <span className="text-xs font-mono text-teal/70">Complete</span>
                        )}
                      </div>
                      <h3 className={`text-lg font-semibold ${textColor}`}>{item.title}</h3>
                      <ul className="mt-3 grid gap-2 text-sm text-slate sm:grid-cols-2 md:grid-cols-3">
                        {item.topics.map((topic) => (
                          <li key={topic} className="flex items-start gap-2">
                            <span className="shrink-0">→</span>
                            <span>{topic}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Connection line to next item */}
                  {index < weeks.length - 1 && (
                    <div className="absolute -bottom-3 left-[0.75rem] h-6 w-0.5 bg-gradient-to-b from-teal/30 to-graphite/10" />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* About */}
      <section className="border-t border-card-border px-6 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-4xl space-y-8">
          <h2 className="text-2xl font-bold leading-tight">About</h2>
          <div className="space-y-6 text-lg leading-relaxed text-slate">
            <p>
              This Data Engineer BootCamp curriculum spans six weeks of hands-on data engineering
              training. Starting from foundational concepts like Docker and cloud infrastructure, it
              progresses through modern data stack tools including Prefect, BigQuery, dbt, Apache
              Spark, and Kafka.
            </p>
            <p>
              Each week builds on core principles: data flows through pipelines, schemas matter,
              testing and documentation are essential, and every system has trade-offs. The course
              materials include week-by-week lessons, practical examples, and a capstone project to
              solidify understanding.
            </p>
            <p>
              See the original course at{" "}
              <a
                href="https://dezoomcamp.streamlit.app/"
                className="font-medium text-teal underline-offset-4 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                dezoomcamp.streamlit.app
              </a>
              .
            </p>
            <div className="pt-4">
              <a
                href="/tour"
                className="inline-flex items-center justify-center rounded-lg border border-teal/50 bg-teal/10 px-6 py-3 font-medium text-teal hover:bg-teal/20 transition-colors"
              >
                Take the Guided Tour
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-card-border px-6 py-12 sm:px-8 text-center text-sm text-slate">
        <div className="mx-auto max-w-4xl space-y-3">
          <p>
            Built with Next.js and Tailwind CSS. Course materials in{" "}
            <code className="font-mono bg-graphite/10 px-2 py-1 rounded">original/</code>
          </p>
          <p>
            <a
              href="https://rin.contact"
              className="text-teal underline-offset-4 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              rin.contact
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}
