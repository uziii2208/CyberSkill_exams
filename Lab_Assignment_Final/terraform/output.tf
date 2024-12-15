# Outputs
output "public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.app_instance.public_ip
}
