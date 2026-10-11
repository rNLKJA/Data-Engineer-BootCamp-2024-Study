"use client";

export default function Home() {
  return (
    <div className="space-y-20 py-20">
      {/* Hero */}
      <section className="mx-auto max-w-4xl space-y-6 px-4 text-center">
        <h1 className="text-5xl font-black tracking-tight">
          Data Engineer
          <br />
          Boot Camp
        </h1>
        <p className="text-xl text-gray-600">
          Learn data engineering fundamentals through hands-on lessons spanning orchestration,
          warehousing, analytics, batch and stream processing.
        </p>
      </section>

      {/* Curriculum */}
      <section className="mx-auto max-w-5xl px-4">
        <h2 className="mb-12 text-2xl font-black">Curriculum</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {[
            {
              week: "Week 1",
              title: "Introduction & Prerequisites",
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
              topics: [
                "Introduction to Kafka",
                "Schemas with Avro",
                "Kafka Streams",
                "Kafka Connect and KSQL",
                "Real-time data pipelines",
              ],
            },
          ].map((item) => (
            <div key={item.week} className="border border-gray-300 bg-white p-6">
              <div className="mb-2 text-sm font-mono text-red-500">{item.week}</div>
              <h3 className="mb-3 text-lg font-bold">{item.title}</h3>
              <ul className="space-y-1 text-sm text-gray-600">
                {item.topics.map((topic) => (
                  <li key={topic} className="flex items-start">
                    <span className="mr-2">→</span>
                    {topic}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* About */}
      <section className="mx-auto max-w-4xl border-t border-gray-300 px-4 pt-20">
        <h2 className="mb-8 text-2xl font-black">About</h2>
        <div className="space-y-4 text-gray-700">
          <p>
            This Data Engineer BootCamp curriculum spans seven weeks of hands-on data engineering
            training. Starting from foundational concepts like Docker and cloud infrastructure, it
            progresses through modern data stack tools like dbt, Apache Spark, and Kafka.
          </p>
          <p>
            Each week builds on core principles: data flows through pipelines, schemas matter,
            testing and documentation are essential, and every system has trade-offs.
          </p>
          <p>
            The course materials include week-by-week lessons, practical examples, and a capstone
            project to solidify understanding. See the original course at{" "}
            <a
              href="https://dezoomcamp.streamlit.app/"
              className="text-red-500 underline hover:text-red-600"
              target="_blank"
              rel="noopener noreferrer"
            >
              dezoomcamp.streamlit.app
            </a>
            .
          </p>
          <p className="pt-4">
            <a
              href="/tour"
              className="inline-block border border-red-500 bg-white px-6 py-3 font-bold text-red-500 hover:bg-red-50"
            >
              Take the Guided Tour
            </a>
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="mx-auto max-w-5xl border-t border-gray-300 px-4 py-12 text-center text-sm text-gray-600">
        <p>
          Built with Next.js. Read the full course materials in{" "}
          <code className="bg-gray-100 px-2 py-1">original/</code>
        </p>
        <p className="mt-4">
          <a
            href="https://rin.contact"
            className="underline hover:text-gray-900"
            target="_blank"
            rel="noopener noreferrer"
          >
            rin.contact
          </a>
        </p>
      </footer>
    </div>
  );
}
