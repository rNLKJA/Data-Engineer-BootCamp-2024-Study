output "image_id" {
  description = "ID of the built pipeline image."
  value       = docker_image.pipeline.image_id
}

output "container_name" {
  description = "Name of the container that ran the pipeline."
  value       = docker_container.pipeline_run.name
}

output "exit_code" {
  description = "Exit code of the pipeline container (0 means the flow completed)."
  value       = docker_container.pipeline_run.exit_code
}

output "container_logs" {
  description = "Full output of the pipeline run inside the container."
  value       = docker_container.pipeline_run.container_logs
}
