# -------------------------------
# Provider AWS
# -------------------------------
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.4.0"
}

provider "aws" {
  region = "us-east-1"  # change selon ta région
}

# -------------------------------
# Variables
# -------------------------------
variable "key_name" {
  description = "Nom de la clé SSH pour accéder à l'instance EC2"
  type        = string
}

variable "public_key_path" {
  description = "Chemin vers la clé publique SSH"
  type        = string
}

# -------------------------------
# Key Pair
# -------------------------------
resource "aws_key_pair" "deployer" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

# -------------------------------
# Security Group
# -------------------------------
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-docker-sg"
  description = "Allow SSH, HTTP, HTTPS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["YOUR_IP/32"] # remplace par ton IP
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# -------------------------------
# VPC Data
# -------------------------------
# 1️⃣ Create a new VPC
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "my-vpc-ecom"
  }
}

# 2️⃣ Create a public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = data.aws_availability_zones.available.names[0]
  tags = {
    Name = "my-public-subnet"
  }
}

# Fetch AZs
data "aws_availability_zones" "available" {}


# 3️⃣ Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name = "my-igw"
  }
}

# 4️⃣ Route Table for Public Subnet
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.my_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "my-public-rt"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}


# -------------------------------
# EC2 Instance
# -------------------------------
resource "aws_instance" "docker_ec2" {
  ami                         = "ami-0c02fb55956c7d316" # Ubuntu 22.04 LTS, change selon région
  instance_type               = "t3.medium"
  key_name                    = aws_key_pair.deployer.key_name
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true
  root_block_device {
    volume_size = 30  # 30 GB
    volume_type = "gp3"
  }

  # -------------------------------
  # User data : installer Docker + Docker Compose
  # -------------------------------
  user_data = <<-EOF
            #!/bin/bash
            set -e

            # -------------------------------
            # Mise à jour du système
            # -------------------------------
            apt update -y
            apt upgrade -y
            apt install -y apt-transport-https ca-certificates curl gnupg lsb-release nginx

            # -------------------------------
            # Installer Docker et Docker Compose
            # -------------------------------
            mkdir -p /etc/apt/keyrings
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
            apt update -y
            apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

            # Ajouter ubuntu au groupe docker
            usermod -aG docker ubuntu

            # Activer Docker au démarrage
            systemctl enable docker
            systemctl start docker

            # -------------------------------
            # Configurer Nginx comme reverse proxy
            # -------------------------------
            cat > /etc/nginx/sites-available/reverse-proxy.conf <<EOL
            server {
                listen 80;

                # Frontend
                location / {
                    proxy_pass http://localhost:8000;
                    proxy_set_header Host \$host;
                    proxy_set_header X-Real-IP \$remote_addr;
                    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto \$scheme;
                }

                # Filebrowser
                location /files/ {
                    proxy_pass http://localhost:8080/;
                    proxy_set_header Host \$host;
                    proxy_set_header X-Real-IP \$remote_addr;
                    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto \$scheme;
                }
            }
            EOL

            # Activer la config Nginx
            ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/
            nginx -t
            systemctl restart nginx
            systemctl enable nginx
            EOF


  tags = {
    Name = "docker-ec2-instance"
  }
}

# -------------------------------
# Outputs
# -------------------------------
output "ec2_public_ip" {
  value = aws_instance.docker_ec2.public_ip
  description = "IP publique de l'instance EC2"
}




# 1️⃣ Noms simples et professionnels
# shoply.com
# eBoutique.com
# clickstore.com
# myshoponline.com
# buyzone.com

# 2️⃣ Noms créatifs / modernes
# Zento.com
# Shopora.com
# Buylio.com
# Cartsy.com
# NexoShop.com