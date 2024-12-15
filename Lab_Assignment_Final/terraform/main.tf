# Provider Configuration
provider "aws" {
  region = "ap-southeast-1" # Adjust to your preferred AWS region
}

# Key Pair
resource "aws_key_pair" "deployer_key" {
  key_name   = "deployer_key"
  public_key = file("~/.ssh/id_rsa.pub") # Update this to the path of your public SSH key
}

# Security Group
resource "aws_security_group" "app_sg" {
  name_prefix = "app-sg-"

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict to specific IP in production
  }

  ingress {
    description = "Allow application traffic"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict to specific IP in production
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "app_instance" {
  ami           = "ami-07c1207a9d40bc3bd" # Ubuntu 24.04 LTS AMI for ap-southeast-1 region
  instance_type = "t2.micro" # Use free-tier eligible instance type
  key_name      = aws_key_pair.deployer_key.key_name

  security_group_names = [aws_security_group.app_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get upgrade -y
              apt-get install -y docker.io git
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              su - ubuntu -c "git clone https://github.com/arifsetiawan/node-test-sample.git"
              cd /home/ubuntu/node-test-sample
              docker build -t node-app .
              docker run -d -p 8000:8000 --name node-app node-app
            EOF

  tags = {
    Name = "NodeAppInstance"
  }
}

# Outputs
output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_instance.public_ip
}
