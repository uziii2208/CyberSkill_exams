variable "app_image_name" {
  description = "The Docker image name for the application"
  default     = "node:20.17.0"
}

variable "app_name" {
  description = "Name of the Docker container"
  default     = "my_node_app"
}

variable "app_host_port" {
  description = "Port on the host machine to expose the application"
  default     = 8000
}

variable "app_container_port" {
  description = "Port inside the container for the application"
  default     = 8000
}
