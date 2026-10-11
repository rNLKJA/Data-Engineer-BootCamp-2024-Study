<p><a target="_blank" href="https://app.eraser.io/workspace/bqYqyZzge8nO3UiGLlIt" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

# Data Engineer BootCamp

A comprehensive data engineering curriculum brought to life as an interactive web application.

**Live demo:** [data-engineer-bootcamp-pink.vercel.app](https://data-engineer-bootcamp-pink.vercel.app)

## Showcase

The site presents the full data engineering curriculum across six weeks:

| | |
| --- | --- |
| **Landing Page** | Hero section introducing the BootCamp with an overview of what is covered |
| **Curriculum Grid** | Six weeks of data engineering topics: infrastructure, orchestration, warehousing, analytics, batch and stream processing |
| **About Section** | Course philosophy and link to the original dezoomcamp resources |
| **Guided Tour** | Walkthrough of the course structure and learning resources |

## Overview

This Data Engineer BootCamp curriculum spans six intensive weeks of hands-on training in modern data engineering practices:

- **Week 1: Introduction & Prerequisites** - GCP, Docker, Terraform, and local infrastructure setup
- **Week 2: Workflow Orchestration** - Data lakes and Prefect orchestration patterns
- **Week 3: Data Warehouse** - BigQuery fundamentals and best practices
- **Week 4: Analytics Engineering** - dbt and data transformation workflows
- **Week 5: Batch Processing** - Apache Spark and distributed computing
- **Week 6: Stream Processing** - Kafka and real-time data pipelines

Every principle builds on understanding that data flows through pipelines, schemas matter, testing and documentation are essential, and every system involves trade-offs.

## Features

- **Responsive Design** - Clean, modern interface optimised for desktop and mobile
- **Nothing-OS Aesthetic** - Minimalist design with white/black palette and red accent (#FF3C3C)
- **Fast Static Site** - Built with Next.js 16 and prerendered at build time
- **Accessible** - Semantic HTML and keyboard navigation
- **CI/CD Ready** - GitHub Actions workflow (lint, typecheck, test, build)

## Tech Stack

| Layer | Technology |
| --- | --- |
| Framework | Next.js 16 (App Router) |
| Runtime | React 19 |
| Styling | Tailwind CSS v4 |
| Language | TypeScript 5 |
| Testing | Vitest |
| CI/CD | GitHub Actions |
| Hosting | Vercel (free tier) |

## Repository Structure

```
Data-Engineer-BootCamp-2024-Study/
├── README.md                 (this file)
├── LICENSE
├── .github/workflows/ci.yml  (lint, typecheck, test, build)
├── original/                 (2024 course materials)
│   ├── week1_introduction_and_prerequisites/
│   ├── week2_workflow_orchestration/
│   ├── week3_data_warehouse/
│   ├── week4_analytics_engineering/
│   ├── week5_batch_processing/
│   ├── week6_stream_processing/
│   └── project/
└── web/                      (Next.js app, Vercel root)
    ├── app/                  (pages: /, /tour)
    ├── public/               (static assets)
    ├── src/                  (tests)
    ├── package.json
    ├── tsconfig.json
    └── next.config.ts
```

## Local Development

Requirements: Node 20+ and npm.

```bash
cd web
npm install --legacy-peer-deps
npm run dev              # http://localhost:3860
npm run lint && npm run format:check && npm run typecheck && npm run build
```

## Deployment

Production is hosted on Vercel, deployed from `web/`:

```bash
cd web
vercel link --yes --project data-engineer-bootcamp
vercel deploy --prod --yes
```

The site deploys automatically on pushes to the default branch after CI passes.

## About

This is a revival of the 2024 Data Engineer BootCamp study materials, transformed into a polished web experience. The original course materials remain unchanged in `original/` with their full git history preserved. The website is a complete rewrite: designed for modern browsers, optimised for learning, and deployed on Vercel's free tier.

The design follows the Nothing-OS aesthetic: minimal, functional, and built for clarity. Every element serves a purpose. See [rin.contact](https://rin.contact) for more similar projects.

## License

MIT. Data and course materials remain under their original licences.
