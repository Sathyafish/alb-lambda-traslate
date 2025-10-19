variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "lambda-alb-translate"
}

variable "vpc_id" {
  description = "ID of the existing VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs of the existing public subnets"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "IDs of the existing private subnets"
  type        = list(string)
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "lambda_memory_size" {
  description = "Memory size for Lambda function"
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Timeout for Lambda function"
  type        = number
  default     = 30
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate to use for HTTPS listener"
  type        = string
  default     = "dev"
}
