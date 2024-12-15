# Define outputs for the infrastructure

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_instance.public_ip
}

output "app_security_group_id" {
  description = "ID of the security group for the application"
  value       = aws_security_group.app_sg.id
}

output "instance_id" {
  description = "ID of the created EC2 instance"
  value       = aws_instance.app_instance.id
}

output "app_container_name" {
  description = "Name of the Docker container running the app"
  value       = var.app_name
}
