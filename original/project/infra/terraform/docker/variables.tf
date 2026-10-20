variable "docker_host" {
  description = "Docker daemon address."
  type        = string
  default     = "unix:///var/run/docker.sock"
}

variable "data_dir" {
  description = "Host folder mounted at /data in the container. Empty means original/project/data (must exist)."
  type        = string
  default     = ""
}

variable "image_name" {
  description = "Name of the pipeline image."
  type        = string
  default     = "sa-crash-pipeline"
}

variable "image_tag" {
  description = "Tag of the pipeline image."
  type        = string
  default     = "local"
}

variable "container_name" {
  description = "Name of the one-off pipeline container."
  type        = string
  default     = "sa-crash-pipeline-run"
}

variable "buildx_builder" {
  description = "buildx builder used for the image build ('default' is the docker driver builder)."
  type        = string
  default     = "default"
}
