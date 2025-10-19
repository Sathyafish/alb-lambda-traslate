output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer"
  value       = aws_lb.main.zone_id
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = aws_lb.main.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.translate.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.translate.arn
}

output "lambda_function_invoke_arn" {
  description = "Invoke ARN of the Lambda function"
  value       = aws_lambda_function.translate.invoke_arn
}

output "vpc_id" {
  description = "ID of the VPC used"
  value       = data.aws_vpc.existing.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets used"
  value       = data.aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets used"
  value       = data.aws_subnet.private[*].id
}

output "api_endpoint" {
  description = "API endpoint URL"
  value       = "http://${aws_lb.main.dns_name}"
}

output "health_check_endpoint" {
  description = "Health check endpoint URL"
  value       = "http://${aws_lb.main.dns_name}/health"
}

output "translate_endpoint" {
  description = "Translation endpoint URL"
  value       = "http://${aws_lb.main.dns_name}/translate"
}
