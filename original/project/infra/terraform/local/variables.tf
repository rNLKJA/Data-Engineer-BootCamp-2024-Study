variable "data_dir" {
  description = "Root folder for the landing zone, lake and warehouse. Empty means original/project/data."
  type        = string
  default     = ""
}

variable "warehouse_file" {
  description = "File name of the DuckDB warehouse inside the warehouse zone."
  type        = string
  default     = "sa_crash.duckdb"

  validation {
    condition     = can(regex("^[A-Za-z0-9_.-]+\\.duckdb$", var.warehouse_file))
    error_message = "warehouse_file must be a plain file name ending in .duckdb."
  }
}

variable "dbt_threads" {
  description = "Threads dbt-duckdb may use."
  type        = number
  default     = 4

  validation {
    condition     = var.dbt_threads >= 1 && var.dbt_threads <= 16
    error_message = "dbt_threads must be between 1 and 16."
  }
}
