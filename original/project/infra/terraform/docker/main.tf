# Containerised run of the SA road crash pipeline, managed with Terraform.
#
# Builds the project Dockerfile into an image and runs the whole Prefect flow
# once as a container with the data folder bind-mounted at /data. Terraform
# waits for the container to exit (attach = true) and keeps its logs and exit
# code as outputs. This needs a Docker daemon, so it runs in GitHub Actions.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.6"
    }
  }
}

provider "docker" {
  host = var.docker_host
}

locals {
  project_dir = abspath("${path.module}/../../..")
  data_dir    = var.data_dir != "" ? abspath(var.data_dir) : "${local.project_dir}/data"

  # Rebuild the image when anything that goes into it changes.
  image_inputs = sort(concat(
    ["Dockerfile", "requirements.txt", "dbt/dbt_project.yml", "dbt/profiles.yml"],
    tolist(fileset(local.project_dir, "pipeline/*.{py,yml}")),
    tolist(fileset(local.project_dir, "dbt/{models,seeds,tests,macros}/**/*.{sql,yml,csv}")),
  ))
  image_hash = sha1(join("", [for f in local.image_inputs : filesha1("${local.project_dir}/${f}")]))
}

resource "docker_image" "pipeline" {
  name         = "${var.image_name}:${var.image_tag}"
  keep_locally = false

  build {
    context    = local.project_dir
    dockerfile = "Dockerfile"
    builder    = var.buildx_builder
    label = {
      "org.opencontainers.image.title"  = "sa-crash-pipeline"
      "org.opencontainers.image.source" = "https://github.com/rNLKJA/Data-Engineer-BootCamp-2024-Study"
    }
  }

  triggers = {
    image_hash = local.image_hash
  }
}

resource "docker_container" "pipeline_run" {
  name  = var.container_name
  image = docker_image.pipeline.image_id

  # Run once to completion: wait for exit, keep logs and the exit code.
  must_run = false
  attach   = true
  logs     = true
  rm       = false

  env = [
    "SA_CRASH_DATA_DIR=/data",
    "SA_CRASH_DASHBOARD_JSON=/data/export/dashboard-data.json",
    "DBT_USE_COLORS=false",
    "PREFECT_LOGGING_COLORS=false",
  ]

  mounts {
    type   = "bind"
    source = local.data_dir
    target = "/data"
  }
}
