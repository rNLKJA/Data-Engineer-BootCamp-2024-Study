'use client';

export default function TourPage() {
  return (
    <div className="space-y-12 py-20">
      <section className="mx-auto max-w-4xl px-4">
        <h1 className="mb-8 text-4xl font-black">Guided Tour</h1>
        <p className="mb-8 text-gray-600">
          Explore the Data Engineer BootCamp curriculum through an interactive walkthrough.
        </p>

        <div className="space-y-12">
          <div className="border border-gray-300 bg-gray-50 p-8">
            <h2 className="mb-4 text-2xl font-bold">Tour Coming Soon</h2>
            <p className="text-gray-700">
              Interactive video walkthrough showing the curriculum, week-by-week breakdown,
              and course structure. Check back soon for the recorded tour.
            </p>
          </div>

          <div className="space-y-6">
            <h2 className="text-2xl font-black">Course Overview</h2>
            <p className="text-gray-700">
              The Data Engineer BootCamp spans six weeks of intensive training:
            </p>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start">
                <span className="mr-3 font-bold text-red-500">Week 1:</span>
                <span>Introduction & Prerequisites - GCP, Docker, Terraform setup</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3 font-bold text-red-500">Week 2:</span>
                <span>Workflow Orchestration - Data lakes and Prefect</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3 font-bold text-red-500">Week 3:</span>
                <span>Data Warehouse - BigQuery and data modeling</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3 font-bold text-red-500">Week 4:</span>
                <span>Analytics Engineering - dbt and data transformation</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3 font-bold text-red-500">Week 5:</span>
                <span>Batch Processing - Apache Spark and distributed computing</span>
              </li>
              <li className="flex items-start">
                <span className="mr-3 font-bold text-red-500">Week 6:</span>
                <span>Stream Processing - Kafka and real-time pipelines</span>
              </li>
            </ul>
          </div>

          <div className="border-t border-gray-300 pt-8">
            <h2 className="mb-4 text-2xl font-black">Learning Resources</h2>
            <p className="mb-6 text-gray-700">
              All course materials are available in the repository. Start with the
              week-by-week README files to understand the concepts and practicals.
            </p>
            <a
              href="https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block border border-red-500 bg-white px-6 py-3 font-bold text-red-500 hover:bg-red-50"
            >
              View on GitHub
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
