# Define variables for flexibility

variable "aws_region" {
  description = "AWS region"
  default     = "ap-southeast-1" # Adjust this to your preferred region
}

variable "instance_type" {
  description = "Type of EC2 instance to be created"
  default     = "t2.micro" # Free-tier eligible instance type
}

variable "ssh_key_path" {
  description = "Path to your SSH public key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "app_port" {
  description = "Port for the application to listen on"
  default     = 8000
}

variable "app_name" {
  description = "Name of the Docker container for the Node.js app"
  default     = "node-app"
}

variable "docker_image_name" {
  description = "Docker image name for the Node.js app"
  default     = "node-app"
}
