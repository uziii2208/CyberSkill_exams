output "container_name" {
  value = docker_container.app_container.name
}

output "container_ports" {
  value = docker_container.app_container.ports
}

output "container_status" {
  value = docker_container.app_container.status
}
