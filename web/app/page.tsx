import Link from "next/link";
import { BookOpen, Database, GitBranch, Server, Sparkles, Workflow } from "lucide-react";
import { HeroVisual } from "./components/hero-visual";

const WEEKS = [
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
] as const;

const WEEK_ICONS = [BookOpen, Workflow, Database, GitBranch, Server, Sparkles] as const;

export default function HomePage() {
  return (
    <div className="dark flex min-h-dvh flex-col">
      <div className="relative isolate overflow-hidden">
        <div
          aria-hidden="true"
          className="grain absolute inset-0 -z-10 [mask-image:radial-gradient(ellipse_at_top,black,transparent_70%)]"
        />
        <div
          aria-hidden="true"
          className="absolute -top-40 left-1/2 -z-10 size-[42rem] -translate-x-1/2 rounded-full bg-mint/15 blur-3xl"
        />
        <main id="main">
          {/* Hero */}
          <section className="mx-auto grid max-w-6xl items-center gap-14 px-4 pt-20 pb-32 sm:px-6 lg:grid-cols-[1.1fr_0.9fr] lg:pt-32 lg:pb-40">
            <div>
              <p className="kicker text-mint">Data Engineering BootCamp</p>
              <h1 className="mt-6 font-display text-5xl leading-[1.02] font-semibold tracking-tight sm:text-6xl lg:text-7xl">
                Six weeks of hands-on <em className="text-mint not-italic">data engineering</em>.
              </h1>
              <p className="mt-12 max-w-xl text-lg leading-relaxed text-muted-foreground">
                Learn orchestration, warehousing, analytics, batch and stream processing through
                practical training built on real-world tools. From Docker and Terraform through
                Prefect, BigQuery, dbt, Spark and Kafka.
              </p>
              <div className="mt-12 flex flex-wrap gap-3">
                <Link
                  href="#curriculum"
                  className="inline-flex h-12 items-center rounded-full bg-mint px-6 text-[0.95rem] font-medium text-graphite-deep transition-colors hover:bg-mint/90"
                >
                  See the curriculum
                </Link>
                <a
                  href="https://dezoomcamp.streamlit.app/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex h-12 items-center rounded-full border border-white/10 bg-card px-6 text-[0.95rem] font-medium transition-colors hover:border-mint/50"
                >
                  Original course
                </a>
              </div>
              <p className="mt-8 text-sm text-muted-foreground">
                I&apos;m following the DataTalksClub Zoomcamp and keeping my working notes and code here
                as I go. It&apos;s a learn-in-public record, built up one week at a time.
              </p>
            </div>
            <HeroVisual />
          </section>
        </main>
      </div>

      {/* Status */}
      <section aria-labelledby="status" className="border-y border-white/10 bg-gradient-to-br from-graphite-deep/70 to-graphite-deep/50 py-16">
        <h2 id="status" className="sr-only">
          Course progress
        </h2>
        <dl className="mx-auto grid max-w-6xl grid-cols-2 gap-px px-4 sm:px-6 md:grid-cols-3">
          {[
            { label: "Weeks", value: "6", tone: "text-mint" },
            { label: "Complete", value: "1", tone: "text-mint" },
            { label: "Upcoming", value: "5", tone: "text-teal" },
          ].map((s) => (
            <div key={s.label} className="px-2 py-8 text-center md:py-10">
              <dt className="kicker text-muted-foreground">{s.label}</dt>
              <dd className={`mt-2 font-display text-4xl font-semibold sm:text-5xl ${s.tone}`}>
                {s.value}
              </dd>
            </div>
          ))}
        </dl>
      </section>

      {/* Curriculum */}
      <section
        id="curriculum"
        aria-labelledby="curriculum-title"
        className="mx-auto w-full max-w-6xl scroll-mt-20 px-4 py-32 sm:px-6 sm:py-40"
      >
        <p className="kicker text-teal">Curriculum</p>
        <h2
          id="curriculum-title"
          className="mt-3 max-w-2xl font-display text-4xl font-semibold tracking-tight"
        >
          Six weeks, scaffolded by stage.
        </h2>
        <ol className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {WEEKS.map((week, i) => {
            const Icon = WEEK_ICONS[i];
            const isComplete = week.status === "complete";
            return (
              <li
                key={week.week}
                className="relative rounded-3xl border border-white/10 bg-card p-6"
              >
                <span className="absolute top-5 right-6 font-mono text-sm text-muted-foreground">
                  0{i + 1}
                </span>
                <Icon
                  className={`size-7 ${isComplete ? "text-mint" : "text-teal"}`}
                  aria-hidden="true"
                />
                <h3 className="mt-5 font-display text-2xl font-semibold">{week.title}</h3>
                <p className="mt-1 font-mono text-xs text-muted-foreground">{week.week}</p>
                <ul className="mt-3 space-y-1.5">
                  {week.topics.map((topic) => (
                    <li key={topic} className="text-sm leading-relaxed text-muted-foreground">
                      {topic}
                    </li>
                  ))}
                </ul>
                {isComplete && (
                  <div className="mt-4 inline-block rounded-full bg-mint/15 px-3 py-1 text-xs font-medium text-mint">
                    Complete
                  </div>
                )}
              </li>
            );
          })}
        </ol>
      </section>

      {/* About */}
      <section
        id="about"
        aria-labelledby="about-title"
        className="scroll-mt-20 border-t border-white/10 bg-gradient-to-br from-graphite-deep/60 to-graphite-deep/40"
      >
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-32 sm:px-6 sm:py-40 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <p className="kicker text-mint">About this curriculum</p>
            <h2
              id="about-title"
              className="mt-3 font-display text-4xl font-semibold tracking-tight"
            >
              What you will learn.
            </h2>
            <p className="mt-4 leading-relaxed text-muted-foreground">
              This Data Engineer BootCamp curriculum spans six weeks of hands-on data engineering
              training. Starting from foundational concepts like Docker and cloud infrastructure, it
              progresses through modern data stack tools including Prefect, BigQuery, dbt, Apache
              Spark, and Kafka.
            </p>
            <p className="mt-4 leading-relaxed text-muted-foreground">
              Each week builds on core principles: data flows through pipelines, schemas matter,
              testing and documentation are essential, and every system has trade-offs. The course
              materials include week-by-week lessons, practical examples, and a capstone project to
              solidify understanding.
            </p>
          </div>
          <div className="grid content-start gap-4">
            <div className="rounded-2xl border border-white/10 bg-card p-5">
              <h3 className="font-semibold">Course structure</h3>
              <dl className="mt-3 grid gap-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Duration</dt>
                  <dd>6 weeks</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Format</dt>
                  <dd>Hands-on lessons</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Prerequisites</dt>
                  <dd>Basic programming</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Level</dt>
                  <dd>Beginner to intermediate</dd>
                </div>
              </dl>
            </div>
            <div className="rounded-2xl border border-white/10 bg-card p-5">
              <h3 className="font-semibold">Original course</h3>
              <p className="mt-2 text-sm text-muted-foreground">
                See the original course materials and lectures at the official DataTalks.Club
                platform.
              </p>
              <a
                href="https://dezoomcamp.streamlit.app/"
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 inline-block font-mono text-sm text-mint underline-offset-4 hover:underline"
              >
                dezoomcamp.streamlit.app
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* What I learned */}
      <section id="learned" aria-labelledby="learned-title" className="scroll-mt-20 border-t border-white/10">
        <div className="mx-auto max-w-6xl px-4 py-28 sm:px-6 sm:py-36">
          <p className="kicker text-teal">Week 1</p>
          <h2
            id="learned-title"
            className="mt-3 font-display text-4xl font-semibold tracking-tight"
          >
            What I learned.
          </h2>
          <div className="mt-6 max-w-3xl space-y-4 text-[1.05rem] leading-relaxed text-muted-foreground">
            <p>
              Containers solve the &ldquo;it works on my machine&rdquo; problem by packaging an application and
              its environment together. They&apos;re lighter than virtual machines because they share the
              host kernel, making them fast to start and efficient with resources.
            </p>
            <p>
              Docker Compose lets you define multi-container setups in a single YAML file. I spun up
              Postgres and pgAdmin together, then wrote a Python script that downloads NYC taxi data
              as parquet files and loads them month-by-month into the database with SQLAlchemy.
            </p>
            <p>
              The most practical lesson: isolation helps you focus. Each service runs in its own
              container with explicit dependencies, so there&apos;s no conflict between project
              requirements and you can tear everything down cleanly when you&apos;re done.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10">
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
          <div className="flex flex-col items-center gap-4 text-center text-sm text-muted-foreground">
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
        </div>
      </footer>
    </div>
  );
}
