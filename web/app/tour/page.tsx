import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Guided Tour - Data Engineer BootCamp",
  description: "Explore the Data Engineer BootCamp curriculum through an interactive walkthrough.",
};

export default function TourPage() {
  const features = [
    {
      title: "Pipeline Curriculum View",
      description:
        "The curriculum is presented as a data pipeline timeline, with Week 1 marked as complete and subsequent weeks scaffolded by stage. Each week shows its topics and learning outcomes.",
      topics: ["Week-by-week progression", "Status indicators", "Topic overview"],
    },
    {
      title: "Hero and Navigation",
      description:
        "A clean, spacious hero section introduces the bootcamp with a teal accent colour. The sticky header provides navigation to home and the GitHub repository.",
      topics: ["Clear value proposition", "Accessible navigation", "Dark mode support"],
    },
    {
      title: "Course Resources",
      description:
        "The About section explains the course philosophy and links to the original learning materials and the Guided Tour. All links are accessible and clearly marked.",
      topics: ["Course overview", "Resource links", "Call-to-action buttons"],
    },
  ];

  return (
    <div className="flex flex-col bg-background text-foreground">
      {/* Hero */}
      <section className="border-b border-card-border px-6 py-16 sm:px-8 sm:py-24 md:py-32">
        <div className="mx-auto max-w-4xl space-y-8">
          <div className="space-y-4">
            <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-5xl md:text-6xl">
              Guided Tour
            </h1>
          </div>
          <p className="max-w-2xl text-lg leading-relaxed text-slate">
            Explore the Data Engineer BootCamp through an interactive walkthrough of the key features
            and course structure. This tour covers the curriculum layout, navigation, and learning
            resources.
          </p>
        </div>
      </section>

      {/* Tour Features */}
      <section className="px-6 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-4xl">
          <div className="mb-12">
            <h2 className="text-2xl font-bold leading-tight">Key Features</h2>
          </div>

          <div className="space-y-8">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="overflow-hidden rounded-lg border border-card-border bg-card-bg p-8"
              >
                <div className="space-y-4">
                  <div>
                    <div className="text-sm font-mono text-teal uppercase tracking-wider">
                      Part {idx + 1}
                    </div>
                    <h3 className="mt-2 text-2xl font-semibold text-foreground">{feature.title}</h3>
                  </div>
                  <p className="text-lg leading-relaxed text-slate">{feature.description}</p>
                  <div className="pt-4">
                    <p className="text-sm font-mono uppercase tracking-wider text-graphite mb-2">
                      Highlights
                    </p>
                    <ul className="space-y-2">
                      {feature.topics.map((topic) => (
                        <li key={topic} className="flex items-start gap-3 text-sm text-slate">
                          <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-teal" />
                          <span>{topic}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Course Overview */}
      <section className="border-t border-card-border px-6 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-4xl space-y-8">
          <h2 className="text-2xl font-bold leading-tight">Course Outline</h2>
          <div className="space-y-4">
            {[
              {
                week: "Week 1",
                title: "Introduction & Prerequisites",
                topics: "GCP, Docker, Terraform setup",
              },
              {
                week: "Week 2",
                title: "Workflow Orchestration",
                topics: "Data lakes and Prefect",
              },
              {
                week: "Week 3",
                title: "Data Warehouse",
                topics: "BigQuery and data modeling",
              },
              {
                week: "Week 4",
                title: "Analytics Engineering",
                topics: "dbt and data transformation",
              },
              {
                week: "Week 5",
                title: "Batch Processing",
                topics: "Apache Spark and distributed computing",
              },
              {
                week: "Week 6",
                title: "Stream Processing",
                topics: "Kafka and real-time pipelines",
              },
            ].map((item) => (
              <div
                key={item.week}
                className="flex gap-4 border-l-2 border-teal/30 pl-4 py-2"
              >
                <div className="flex-shrink-0">
                  <span className="inline-block rounded bg-teal/10 px-3 py-1 text-sm font-mono font-semibold text-teal">
                    {item.week}
                  </span>
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground">{item.title}</h4>
                  <p className="text-sm text-slate">{item.topics}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Getting Started */}
      <section className="border-t border-card-border px-6 py-16 sm:px-8 sm:py-24">
        <div className="mx-auto max-w-4xl space-y-8">
          <h2 className="text-2xl font-bold leading-tight">Getting Started</h2>
          <div className="space-y-6 text-lg leading-relaxed text-slate">
            <p>
              All course materials are hosted in the GitHub repository. Each week includes detailed
              lessons, practical exercises, and real-world examples. The curriculum builds
              progressively from foundational concepts to advanced data engineering patterns.
            </p>
            <p>
              The bootcamp emphasises hands-on learning through projects and real tools used in
              production data engineering. By completing all six weeks, you will have built a
              complete understanding of modern data stack fundamentals.
            </p>
            <div className="pt-4 flex gap-4">
              <a
                href="/"
                className="inline-flex items-center justify-center rounded-lg border border-teal/50 bg-teal/10 px-6 py-3 font-medium text-teal hover:bg-teal/20 transition-colors"
              >
                Back to Home
              </a>
              <a
                href="https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center rounded-lg border border-graphite/30 bg-graphite/5 px-6 py-3 font-medium text-foreground hover:bg-graphite/10 transition-colors"
              >
                View on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-card-border px-6 py-12 sm:px-8 text-center text-sm text-slate">
        <div className="mx-auto max-w-4xl space-y-3">
          <p>
            Built with Next.js and Tailwind CSS. Course materials in the GitHub repository.
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
