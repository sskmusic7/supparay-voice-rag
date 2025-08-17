#!/bin/bash

# Google Cloud Functions Deployment Script
# This script deploys the Ray AI Chat function to Google Cloud Functions

set -e

# Configuration
PROJECT_ID="supparay-voice-rag"  # Change this to your project ID
REGION="us-central1"             # Change this to your preferred region
FUNCTION_NAME="ray-ai-chat"
RUNTIME="python311"
MEMORY="1GB"
TIMEOUT="540s"  # 9 minutes (max for free tier)
MAX_INSTANCES="10"

echo "🚀 Deploying Ray AI Chat to Google Cloud Functions..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Function: $FUNCTION_NAME"
echo "Runtime: $RUNTIME"
echo "Memory: $MEMORY"
echo "Timeout: $TIMEOUT"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: Not authenticated with gcloud."
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo "📋 Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Deploy the function
echo "🚀 Deploying function..."
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=$RUNTIME \
    --region=$REGION \
    --source=. \
    --entry-point=chat \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --max-instances=$MAX_INSTANCES \
    --set-env-vars="GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION" \
    --set-env-vars="GOOGLE_APPLICATION_CREDENTIALS_JSON=$(cat ~/.config/gcloud/application_default_credentials.json | base64 -w 0)"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Function URL:"
gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(serviceConfig.uri)"

echo ""
echo "📊 Function Status:"
gcloud functions describe $FUNCTION_NAME --region=$REGION --format="value(state)"

echo ""
echo "🔧 To update environment variables (like credentials), run:"
echo "gcloud functions deploy $FUNCTION_NAME --gen2 --runtime=$RUNTIME --region=$REGION --source=. --entry-point=chat --trigger-http --allow-unauthenticated --memory=$MEMORY --timeout=$TIMEOUT --max-instances=$MAX_INSTANCES --set-env-vars=\"GOOGLE_APPLICATION_CREDENTIALS_JSON=\$(cat ~/.config/gcloud/application_default_credentials.json | base64 -w 0)\""

echo ""
echo "📝 To view logs:"
echo "gcloud functions logs read $FUNCTION_NAME --region=$REGION --limit=50"
