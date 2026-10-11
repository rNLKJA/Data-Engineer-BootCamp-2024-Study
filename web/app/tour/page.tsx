import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Guided Tour - Data Engineer BootCamp",
  description: "Explore the Data Engineer BootCamp curriculum through an interactive walkthrough.",
};

export default function TourPage() {
  const videos = [
    {
      title: "Landing Page Tour",
      description: "Explore the Data Engineer BootCamp landing page and hero section.",
      src: "/tour-videos/video-1.mp4",
      transcript: "Landing page introduction, curriculum preview, and call-to-action navigation.",
    },
    {
      title: "Curriculum Deep Dive",
      description: "Discover all six weeks of data engineering topics.",
      src: "/tour-videos/video-2.mp4",
      transcript:
        "Week-by-week curriculum overview covering infrastructure, orchestration, warehousing, analytics, batch and stream processing.",
    },
    {
      title: "About and Resources",
      description: "Learn about the course structure and access learning materials.",
      src: "/tour-videos/video-3.mp4",
      transcript:
        "Course philosophy, learning resources, and how to get started with the bootcamp materials.",
    },
  ];

  return (
    <div className="space-y-12 py-20">
      <section className="mx-auto max-w-4xl px-4">
        <h1 className="mb-8 text-4xl font-black">Guided Tour</h1>
        <p className="mb-8 text-gray-600">
          Explore the Data Engineer BootCamp curriculum through interactive walkthroughs of the key
          features and content areas.
        </p>

        <div className="space-y-12">
          {videos.map((video, idx) => (
            <div key={idx} className="border border-gray-300 bg-white p-6">
              <div className="mb-4 grid gap-6 lg:grid-cols-3">
                <div className="lg:col-span-2">
                  <video
                    controls
                    className="w-full border border-gray-300"
                    poster={`/tour-videos/poster-${idx + 1}.jpg`}
                  >
                    <source src={video.src} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>
                <div className="space-y-2">
                  <h3 className="text-lg font-bold">{video.title}</h3>
                  <p className="text-sm text-gray-600">{video.description}</p>
                </div>
              </div>
              <div className="border-t border-gray-300 pt-4">
                <h4 className="mb-2 text-sm font-bold">Transcript</h4>
                <p className="text-sm text-gray-600">{video.transcript}</p>
              </div>
            </div>
          ))}

          <div className="border-t border-gray-300 pt-8">
            <h2 className="mb-4 text-2xl font-black">Course Overview</h2>
            <p className="mb-6 text-gray-700">
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
              All course materials are available in the repository. Start with the week-by-week
              README files to understand the concepts and practicals.
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
