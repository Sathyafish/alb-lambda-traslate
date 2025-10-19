import json
import boto3
import os
from botocore.exceptions import ClientError

# Initialize clients
region = os.environ.get("AWS_REGION", "us-east-1")
translate_client = boto3.client("translate", region_name=region)
comprehend_client = boto3.client("comprehend", region_name=region)

def lambda_handler(event, context):
    """
    Lambda function for AWS Translate via ALB integration.
    Supports:
      - POST /translate
      - GET  /languages
      - GET  /health
      - OPTIONS
    """

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
    }

    def response(status_code, body):
        return {
            "statusCode": status_code,
            "statusDescription": f"{status_code} {'OK' if status_code == 200 else 'Error'}",
            "isBase64Encoded": False,
            "headers": headers,
            "body": json.dumps(body)
        }

    try:
        http_method = event.get("httpMethod", "GET")
        path = event.get("path", "/")

        if http_method == "OPTIONS":
            return response(200, {"message": "CORS preflight successful"})

        if path == "/health":
            return response(200, {
                "status": "healthy",
                "service": "lambda-alb-translate",
                "request_id": context.aws_request_id
            })

        if path == "/languages" and http_method == "GET":
            return handle_list_languages(response)

        if path == "/translate" and http_method == "POST":
            return handle_translate_request(event, response)

        if path == "/":
            return response(200, {
                "service": "AWS Translate API via Lambda + ALB",
                "version": "2.1.0",
                "endpoints": {
                    "/translate": "POST → Translate text",
                    "/languages": "GET → List supported languages",
                    "/health": "GET → Service health check"
                },
                "example_request": {
                    "text": "Good morning!",
                    "target_language_code": "de"
                }
            })

        return response(404, {"error": f"Path {path} not found"})

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return response(500, {"error": "Internal server error", "message": str(e)})


# -----------------------------
# Helper Handlers
# -----------------------------

def handle_translate_request(event, response):
    """
    Handles POST /translate
    Automatically detects source language if not provided
    """
    try:
        body = json.loads(event.get("body", "{}"))
        text = body.get("text")
        target = body.get("target_language_code")
        source = body.get("source_language_code")

        if not text or not target:
            return response(400, {"error": "Missing required fields: 'text' and 'target_language_code'"})

        # Auto-detect source language if not provided
        if not source:
            detection = comprehend_client.detect_dominant_language(Text=text)
            source = detection["Languages"][0]["LanguageCode"]
            print(f"Detected source language: {source}")

        # Perform translation
        result = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source,
            TargetLanguageCode=target
        )

        return response(200, {
            "original_text": text,
            "translated_text": result["TranslatedText"],
            "source_language_code": result["SourceLanguageCode"],
            "target_language_code": result["TargetLanguageCode"]
        })

    except ClientError as e:
        print(f"AWS Translate error: {str(e)}")
        return response(400, {
            "error": "Translation failed",
            "code": e.response["Error"]["Code"],
            "message": e.response["Error"]["Message"]
        })
    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON in request body"})


def handle_list_languages(response):
    """
    Returns static list of common AWS Translate languages
    """
    languages = [
        {"LanguageCode": "en", "LanguageName": "English"},
        {"LanguageCode": "es", "LanguageName": "Spanish"},
        {"LanguageCode": "fr", "LanguageName": "French"},
        {"LanguageCode": "de", "LanguageName": "German"},
        {"LanguageCode": "it", "LanguageName": "Italian"},
        {"LanguageCode": "pt", "LanguageName": "Portuguese"},
        {"LanguageCode": "zh", "LanguageName": "Chinese (Simplified)"},
        {"LanguageCode": "ja", "LanguageName": "Japanese"},
        {"LanguageCode": "ko", "LanguageName": "Korean"},
        {"LanguageCode": "ar", "LanguageName": "Arabic"}
    ]
    return response(200, {"languages": languages, "count": len(languages)})

