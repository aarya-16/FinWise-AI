#!/bin/bash
# Build script for deployment - builds frontend then starts backend

echo "Building frontend..."
cd ../frontend
npm install
npm run build

echo "Frontend built successfully!"
echo "Starting backend..."
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
