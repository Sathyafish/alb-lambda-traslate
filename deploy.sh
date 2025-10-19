#!/bin/bash

# Lambda ALB Translate Deployment Script

set -e

echo "🚀 Starting deployment of Lambda ALB Translate..."

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install Terraform first."
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "⚠️  terraform.tfvars not found. Creating from example..."
    cp terraform.tfvars.example terraform.tfvars
    echo "📝 Please edit terraform.tfvars with your preferred values before continuing."
    echo "Press Enter to continue or Ctrl+C to exit..."
    read
fi

# Plan the deployment
echo "📋 Planning deployment..."
terraform plan

# Ask for confirmation
echo "🤔 Do you want to proceed with the deployment? (y/N)"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 0
fi

# Apply the configuration
echo "🏗️  Deploying infrastructure..."
terraform apply -auto-approve

# Get outputs
echo "✅ Deployment completed!"
echo ""
echo "📊 Deployment Summary:"
echo "====================="
echo "API Endpoint: $(terraform output -raw api_endpoint)"
echo "Health Check: $(terraform output -raw health_check_endpoint)"
echo "Translate Endpoint: $(terraform output -raw translate_endpoint)"
echo ""
echo "🧪 Test the API:"
echo "curl $(terraform output -raw api_endpoint)/health"
echo ""
echo "🔄 To destroy the infrastructure:"
echo "terraform destroy"
