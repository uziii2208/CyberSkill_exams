# Provider Configuration
provider "aws" {
  region = "us-east-1" # Adjust this to your preferred AWS region
}

# Key Pair
resource "aws_key_pair" "deployer_key" {
  key_name   = "deployer_key"
  public_key = file("~/.ssh/id_rsa.pub") # Adjust this to your public key path
}

# Security Group
resource "aws_security_group" "app_sg" {
  name_prefix = "app-sg-"

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict this in production
  }

  ingress {
    description = "Allow app traffic"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict this in production
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "app_instance" {
  ami           = "ami-047126e50991d067b" # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  key_name      = corbierevn.pem

  security_groups = [corbierevn-wizard-1]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              yum install -y git
              git clone https://github.com/arifsetiawan/node-test-sample.git
              cd node-test-sample
              docker build -t node-app .
              docker run -d -p 8000:8000 --name node-app node-app
            EOF

  tags = {
    Name = "NodeAppInstance"
  }
}

# Outputs
output "instance_public_ip" {
  value = aws_instance.app_instance.public_ip
}
