# Local infrastructure as code for the SA road crash pipeline.
#
# There is no cloud account in this project, so this stack manages the local
# equivalents of what a cloud stack would create: the landing zone and lake
# folders (stand-ins for GCS buckets), the warehouse folder (stand-in for a
# BigQuery dataset), and the rendered configuration the pipeline and dbt read.
# Works with Terraform >= 1.6 or OpenTofu.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.9"
    }
  }
}

locals {
  project_dir = abspath("${path.module}/../../..")
  data_dir    = var.data_dir != "" ? abspath(var.data_dir) : "${local.project_dir}/data"

  zones = {
    landing      = "${local.data_dir}/landing"
    lake_raw     = "${local.data_dir}/lake/raw"
    lake_curated = "${local.data_dir}/lake/curated"
    warehouse    = "${local.data_dir}/warehouse"
    config       = "${local.data_dir}/config"
  }

  warehouse_path = "${local.zones.warehouse}/${var.warehouse_file}"
}

# One marker file per zone; the local provider creates the parent folders.
resource "local_file" "zone_marker" {
  for_each = local.zones

  filename             = "${each.value}/.keep"
  content              = "Managed by infra/terraform/local: ${each.key} zone of the SA road crash pipeline.\n"
  file_permission      = "0644"
  directory_permission = "0755"
}

resource "local_file" "pipeline_env" {
  filename        = "${local.zones.config}/pipeline.env"
  file_permission = "0644"
  content = templatefile("${path.module}/templates/pipeline.env.tftpl", {
    data_dir       = local.data_dir
    landing_dir    = local.zones.landing
    lake_dir       = "${local.data_dir}/lake"
    warehouse_path = local.warehouse_path
    config_dir     = local.zones.config
  })
}

resource "local_file" "dbt_profiles" {
  filename        = "${local.zones.config}/profiles.yml"
  file_permission = "0644"
  content = templatefile("${path.module}/templates/profiles.yml.tftpl", {
    warehouse_path = local.warehouse_path
    threads        = var.dbt_threads
  })
}
