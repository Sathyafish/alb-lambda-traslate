import json
import boto3
import os
from botocore.exceptions import ClientError

# Initialize AWS Translate client
translate_client = boto3.client('translate', region_name=os.environ.get('APP_REGION', 'us-east-1'))

def lambda_handler(event, context):
    """
    Lambda function handler for AWS Translate integration via ALB
    """
    
    # Parse the HTTP request from ALB
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Set default response headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    try:
        # Handle CORS preflight requests
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight successful'})
            }
        
        # Health check endpoint
        if path == '/health':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'lambda-alb-translate',
                    'timestamp': context.aws_request_id
                })
            }
        
        # Translation endpoint
        if path == '/translate':
            if http_method == 'POST':
                return handle_translate_request(event, headers)
            else:
                return {
                    'statusCode': 405,
                    'headers': headers,
                    'body': json.dumps({'error': 'Method not allowed. Use POST for translation.'})
                }
        
        # List supported languages endpoint
        if path == '/languages':
            if http_method == 'GET':
                return handle_list_languages(headers)
            else:
                return {
                    'statusCode': 405,
                    'headers': headers,
                    'body': json.dumps({'error': 'Method not allowed. Use GET for listing languages.'})
                }
        
        # Root endpoint with API documentation
        if path == '/':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'service': 'AWS Translate API via Lambda + ALB',
                    'version': '1.0.0',
                    'endpoints': {
                        'health': 'GET /health',
                        'translate': 'POST /translate',
                        'languages': 'GET /languages'
                    },
                    'usage': {
                        'translate': {
                            'method': 'POST',
                            'body': {
                                'text': 'Text to translate',
                                'source_language_code': 'en',
                                'target_language_code': 'es'
                            }
                        }
                    }
                })
            }
        
        # 404 for unknown paths
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Endpoint not found'})
        }
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def handle_translate_request(event, headers):
    """
    Handle translation requests
    """
    try:
        # Parse request body
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Request body is required'})
            }
        
        # Validate required fields
        required_fields = ['text', 'source_language_code', 'target_language_code']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }
        
        # Call AWS Translate
        response = translate_client.translate_text(
            Text=body['text'],
            SourceLanguageCode=body['source_language_code'],
            TargetLanguageCode=body['target_language_code']
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'translated_text': response['TranslatedText'],
                'source_language_code': response['SourceLanguageCode'],
                'target_language_code': response['TargetLanguageCode'],
                'original_text': body['text']
            })
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'error': 'Translation failed',
                'code': error_code,
                'message': error_message
            })
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }

def handle_list_languages(headers):
    """
    Handle request to list supported languages
    """
    try:
        # Get list of supported languages
        response = translate_client.list_languages()
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'languages': response['Languages'],
                'count': len(response['Languages'])
            })
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'error': 'Failed to list languages',
                'code': error_code,
                'message': error_message
            })
        }
