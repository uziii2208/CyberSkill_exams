provider "docker" {
  host = "npipe:////./pipe/docker_engine" # For Windows; adjust for Linux/Mac
}

variable "app_image_name" {
  default = "node:20.17.0"
}

variable "app_name" {
  default = "my_node_app"
}

variable "app_host_port" {
  default = 8000
}

variable "app_container_port" {
  default = 8000
}

resource "docker_image" "app_image" {
  name = var.app_image_name
}

resource "docker_container" "app_container" {
  image = docker_image.app_image.latest
  name  = var.app_name

  ports {
    internal = var.app_container_port
    external = var.app_host_port
  }

  volumes {
    host_path      = "${path.root}/../scripts"
    container_path = "/app"
  }

  command      = ["npm", "start"]
  working_dir  = "/app"
  environment  = {
    NODE_ENV = "production"
  }

  depends_on = [docker_image.app_image]
}
