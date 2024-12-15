![image](https://github.com/user-attachments/assets/c323ce84-8d14-4ba6-b14a-4c4f1084af34)

# Terraform Configuration for Dockerized Node.js Application

## Objective
This Terraform configuration sets up infrastructure for deploying a Dockerized Node.js application. It includes defining a container, exposing it on a network port, and providing an easily reproducible environment.

## Features
- Defines a Docker container for the Node.js application.
- Exposes the application on a specified port.
- Dynamically configurable using Terraform variables.
- Easy to destroy and recreate the infrastructure.

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Docker**: [Docker Installation Guide](https://docs.docker.com/get-docker/)
2. **Terraform**: [Terraform Installation Guide](https://www.terraform.io/downloads)
3. **Node.js** (optional, if you want to test locally): [Node.js Installation Guide](https://nodejs.org/)

---

## Directory Structure

```
Lab_Assignment_Final/
├── photos/
├── scripts/
│   ├── logs/
│   │   ├── access.log
│   │   ├── analyzed_log.log
│   │   ├── cpu_mem_usage.log
│   │   ├── daily_logs.gz
│   │   ├── script.log
│   └── helloworld.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
```

---

## Terraform Files

### `main.tf`
This file contains the core Terraform configuration, including provider setup, Docker image, and container resource definitions.

### `variables.tf`
Defines input variables to make the configuration dynamic and customizable.

### `outputs.tf`
Outputs information about the infrastructure after provisioning, such as container name and port mappings.

---

## How to Use

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/<your-repo>.git
cd Lab_Assignment_Final/terraform
```

### Step 2: Initialize Terraform
Run the following command to initialize Terraform and download the necessary providers:
```bash
terraform init
```

### Step 3: Validate the Configuration
Ensure the Terraform configuration is valid:
```bash
terraform validate
```

### Step 4: Apply the Configuration
Apply the configuration to create the Docker container:
```bash
terraform apply
```
- When prompted, type `yes` to confirm.

### Step 5: Access the Application
Once the infrastructure is provisioned, access the application using:
```bash
curl http://localhost:8000/
curl http://localhost:8000/getInfo
```
- **Endpoints**:
  - `/`: Returns a description of the lab.
  - `/getInfo`: Returns personal information.

---

## Configurable Variables

The configuration includes variables defined in `variables.tf` that can be adjusted as needed:

| Variable            | Description                               | Default         |
|---------------------|-------------------------------------------|-----------------|
| `app_image_name`    | Docker image name                        | `node:20.17.0`  |
| `app_name`          | Name of the Docker container             | `my_node_app`   |
| `app_host_port`     | Port on the host to expose the container | `8000`          |
| `app_container_port`| Port inside the container                | `8000`          |

To override these values, you can create a `terraform.tfvars` file or pass them directly during the `apply` command:
```bash
terraform apply -var="app_host_port=8080"
```

---

## Outputs

After running `terraform apply`, the following outputs will be displayed:

| Output              | Description                               |
|---------------------|-------------------------------------------|
| `container_name`    | Name of the Docker container             |
| `container_ports`   | Port mappings of the container           |
| `container_status`  | Status of the container                  |

---

## Cleanup

To destroy the infrastructure and clean up resources:
```bash
terraform destroy
```
- Confirm by typing `yes` when prompted.

---

## Notes
- Ensure Docker is running before executing any Terraform commands.
- You can modify the application files in the `scripts` folder and redeploy by rerunning `terraform apply`.

---

## Troubleshooting

1. **Docker Daemon Issues:**
   - Ensure the Docker daemon is running on your system.
   - Check the Docker host configuration in `main.tf`.

2. **Port Conflicts:**
   - Verify that the host port (`8000` by default) is not already in use.
   - Modify the `app_host_port` variable if needed.

3. **Logs:**
   - Application logs are stored in the `scripts/logs` folder. Check these for debugging.

---

## This lab is a complete Terraform configuration for Dockerized Node.js Application

