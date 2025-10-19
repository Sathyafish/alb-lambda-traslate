# Lambda ALB Translate

This Terraform configuration creates an AWS Lambda function integrated with an Application Load Balancer (ALB) that provides translation services using AWS Translate.

## Architecture

- **VPC**: Uses existing VPC (you provide VPC ID)
- **ALB**: Application Load Balancer in existing public subnets for external access
- **Lambda**: Function in existing private subnets with VPC configuration
- **IAM**: Proper roles and policies for Lambda to access AWS Translate
- **Security Groups**: Configured for ALB and Lambda communication

## Features

- RESTful API endpoints for translation
- Health check endpoint
- Language listing endpoint
- CORS support
- Error handling and validation
- VPC security

## API Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `POST /translate` - Translate text
- `GET /languages` - List supported languages

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0 installed
- Python 3.9+ (for Lambda function)

## Usage

1. **Clone and navigate to the directory:**
   ```bash
   cd lambda-alb-translate
   ```

2. **Copy and customize variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your VPC and subnet IDs
   ```

3. **Initialize Terraform:**
   ```bash
   terraform init
   ```

4. **Plan the deployment:**
   ```bash
   terraform plan
   ```

5. **Deploy the infrastructure:**
   ```bash
   terraform apply
   ```

6. **Get the ALB endpoint:**
   ```bash
   terraform output api_endpoint
   ```

## API Usage Examples

### Health Check
```bash
curl http://your-alb-dns-name/health
```

### List Supported Languages
```bash
curl http://your-alb-dns-name/languages
```

### Translate Text
```bash
curl -X POST http://your-alb-dns-name/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "source_language_code": "en",
    "target_language_code": "es"
  }'
```

### Example Response
```json
{
  "translated_text": "¡Hola, mundo!",
  "source_language_code": "en",
  "target_language_code": "es",
  "original_text": "Hello, world!"
}
```

## Configuration

### Variables

- `aws_region`: AWS region for resources (default: us-east-1)
- `project_name`: Name prefix for all resources (default: lambda-alb-translate)
- `vpc_id`: ID of the existing VPC (required)
- `public_subnet_ids`: List of existing public subnet IDs (required)
- `private_subnet_ids`: List of existing private subnet IDs (required)
- `lambda_memory_size`: Memory allocation for Lambda (default: 256)
- `lambda_timeout`: Timeout for Lambda function (default: 30)

### IAM Permissions

The Lambda function requires the following AWS Translate permissions:
- `translate:TranslateText`
- `translate:ListLanguages`
- `translate:DescribeTextTranslationJob`
- `translate:ListTextTranslationJobs`

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

## Security Considerations

- Lambda function runs in your existing private subnets
- ALB is in your existing public subnets with security group restrictions
- IAM roles follow least privilege principle
- Uses your existing VPC for network isolation

## Monitoring

- CloudWatch logs are automatically enabled for the Lambda function
- ALB provides access logs and metrics
- Health checks monitor Lambda function availability

## Troubleshooting

1. **Lambda function not responding**: Check VPC configuration and security groups
2. **ALB health checks failing**: Verify Lambda function is returning 200 status for `/health`
3. **Translation errors**: Check IAM permissions for AWS Translate
4. **CORS issues**: Verify the Lambda function includes proper CORS headers

## Cost Optimization

- ALB charges apply for load balancer hours and LCU usage
- Lambda charges for execution time and memory
- AWS Translate charges per character translated
- Consider using NAT Gateway for private subnet internet access (should be configured in your existing VPC)
