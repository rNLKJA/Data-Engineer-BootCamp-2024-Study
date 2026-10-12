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
      {/* Hero Section */}
      <section className="relative overflow-hidden border-b border-card-border/50">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 right-0 h-80 w-80 rounded-full bg-teal/5 blur-3xl" />
        </div>

        <div className="relative mx-auto w-full max-w-6xl px-6 py-24 sm:px-8 md:py-40">
          <div className="space-y-8 max-w-3xl">
            <div className="space-y-4">
              <p className="text-xs font-mono tracking-widest uppercase text-teal">
                Six Week Curriculum
              </p>
              <h1 className="text-5xl font-bold leading-tight tracking-tight sm:text-6xl md:text-7xl">
                Data Engineer BootCamp
              </h1>
            </div>
            <p className="text-lg leading-relaxed text-slate max-w-2xl">
              Learn data engineering fundamentals through hands-on lessons spanning orchestration,
              warehousing, analytics, batch and stream processing. Six weeks of practical training
              built on real-world tools and patterns.
            </p>
          </div>
        </div>
      </section>

      {/* Pipeline Timeline */}
      <section className="mx-auto w-full max-w-6xl px-6 py-20 sm:px-8 md:py-28">
        <div className="mb-16 space-y-3">
          <h2 className="text-3xl font-bold leading-tight">Curriculum</h2>
          <p className="text-sm text-slate">Six weeks, scaffolded by stage</p>
        </div>

        {/* Pipeline visual with stages */}
        <div className="relative">
          {/* Connecting line behind all stages */}
          <div className="absolute left-[1.125rem] top-8 bottom-0 w-0.5 bg-gradient-to-b from-teal/60 via-teal/30 to-graphite/10" />

          <div className="space-y-4 relative z-10">
            {weeks.map((item, index) => {
              const isComplete = item.status === "complete";
              const isScaffolded = item.status === "upcoming";

              return (
                <div key={item.week} className="group relative">
                  {/* Stage indicator and card */}
                  <div
                    className={`flex gap-4 rounded-xl border transition-all duration-200 ${
                      isComplete
                        ? "border-teal/40 bg-teal/8 hover:border-teal/60 hover:bg-teal/12"
                        : "border-graphite/20 bg-graphite/5 hover:border-graphite/30 hover:bg-graphite/8"
                    }`}
                  >
                    {/* Status dot on connecting line */}
                    <div className="flex flex-col items-center pt-5 pl-4">
                      <div
                        className={`h-3 w-3 rounded-full ring-4 transition-all ${
                          isComplete ? "bg-teal ring-background" : "bg-graphite/50 ring-background"
                        }`}
                      />
                    </div>

                    {/* Card content */}
                    <div className="flex-1 px-4 py-5 min-w-0">
                      <div className="flex flex-col gap-4">
                        {/* Header with stage label and status */}
                        <div className="flex items-center justify-between gap-3">
                          <div className="flex items-center gap-3">
                            <span className="text-xs font-mono font-semibold tracking-wider text-teal">
                              {item.week}
                            </span>
                            {isComplete && (
                              <span className="text-xs font-mono font-medium text-teal/70 px-2 py-1 bg-teal/15 rounded">
                                Complete
                              </span>
                            )}
                            {isScaffolded && index > 0 && (
                              <span className="text-xs font-mono font-medium text-graphite/60 px-2 py-1 bg-graphite/10 rounded">
                                Scaffolded
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Week title */}
                        <h3
                          className={`text-xl font-semibold leading-tight ${
                            isComplete ? "text-foreground" : "text-graphite"
                          }`}
                        >
                          {item.title}
                        </h3>

                        {/* Topic chips */}
                        <div className="flex flex-wrap gap-2">
                          {item.topics.map((topic) => (
                            <span
                              key={topic}
                              className={`text-xs font-medium px-3 py-1.5 rounded-full whitespace-nowrap ${
                                isComplete ? "bg-teal/15 text-teal" : "bg-graphite/10 text-graphite"
                              }`}
                            >
                              {topic}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* About */}
      <section className="border-t border-card-border/50 mx-auto w-full max-w-6xl px-6 py-20 sm:px-8 md:py-28">
        <div className="space-y-12">
          <div className="space-y-4">
            <h2 className="text-3xl font-bold leading-tight">About</h2>
            <p className="text-sm text-slate">What you will learn</p>
          </div>

          <div className="space-y-6 text-base leading-relaxed text-slate max-w-2xl">
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
                className="font-semibold text-teal hover:text-teal/80 underline underline-offset-2 transition-colors"
                target="_blank"
                rel="noopener noreferrer"
              >
                dezoomcamp.streamlit.app
              </a>
              .
            </p>

            <div className="pt-4 flex gap-3">
              <a
                href="/tour"
                className="inline-flex items-center justify-center rounded-lg border border-teal/50 bg-teal/10 px-5 py-2.5 font-medium text-teal hover:bg-teal/20 hover:border-teal/70 transition-colors text-sm"
              >
                Take the Guided Tour
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-card-border/50 mx-auto w-full max-w-6xl px-6 py-12 sm:px-8 text-center text-xs text-graphite/70">
        <div className="space-y-3">
          <p>
            Built with Next.js and Tailwind CSS. Course materials in{" "}
            <code className="font-mono bg-graphite/10 px-2 py-0.5 rounded text-graphite">
              original/
            </code>
          </p>
          <p>
            <a
              href="https://rin.contact"
              className="text-teal hover:text-teal/80 underline underline-offset-2 transition-colors"
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
