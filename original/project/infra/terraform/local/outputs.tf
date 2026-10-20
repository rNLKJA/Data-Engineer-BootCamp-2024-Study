output "data_dir" {
  description = "Root of the pipeline data folders."
  value       = local.data_dir
}

output "zones" {
  description = "Landing, lake, warehouse and config folders managed by this stack."
  value       = local.zones
}

output "warehouse_path" {
  description = "DuckDB file the dbt profile points at."
  value       = local.warehouse_path
}

output "pipeline_env_file" {
  description = "Source this file to point the pipeline and dbt at these folders."
  value       = local_file.pipeline_env.filename
}

output "dbt_profiles_dir" {
  description = "Folder holding the rendered profiles.yml (use as DBT_PROFILES_DIR)."
  value       = dirname(local_file.dbt_profiles.filename)
}
