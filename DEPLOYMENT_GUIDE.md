# ML Service Deployment Guide

This guide covers different options for deploying your FastAPI ML service for signature verification.

## Deployment Options

### Option 1: Railway (Recommended for ML Services)

Railway is excellent for Python ML applications with large dependencies like TensorFlow.

#### Steps:

1. **Create Railway Account**

   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**

   - Connect your GitHub repository
   - Select the `ml-service` folder as the root directory
   - Railway will auto-detect it's a Python app

3. **Set Environment Variables**

   ```env
   API_HOST=0.0.0.0
   API_PORT=8000
   DEBUG=False
   ALLOWED_ORIGINS=https://plp-document-authentication-web.vercel.app,http://localhost:3000
   SECRET_KEY=your-production-secret-key
   CONFIDENCE_THRESHOLD=0.75
   SUPABASE_URL=your-supabase-url
   SUPABASE_ANON_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_KEY=your-supabase-service-key
   ```

4. **Upload Model File**
   - Railway will build and deploy automatically
   - Make sure `cnn_sign_model.h5` is in the ml-service directory

### Option 2: Render

Good alternative for Python applications.

#### Steps:

1. **Create Render Account**

   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**

   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python run.py`
   - Set root directory: `ml-service`

3. **Set Environment Variables**
   ```env
   API_HOST=0.0.0.0
   API_PORT=8000
   DEBUG=False
   ALLOWED_ORIGINS=https://plp-document-authentication-web.vercel.app
   SECRET_KEY=your-production-secret-key
   CONFIDENCE_THRESHOLD=0.75
   ```

### Option 3: Heroku

Traditional option, but requires some configuration for TensorFlow.

#### Steps:

1. **Install Heroku CLI**

   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**

   ```bash
   cd ml-service
   heroku create your-ml-service-name
   ```

3. **Create Procfile**

   ```bash
   echo "web: python run.py" > Procfile
   ```

4. **Set Environment Variables**

   ```bash
   heroku config:set API_HOST=0.0.0.0
   heroku config:set API_PORT=$PORT
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_ORIGINS=https://plp-document-authentication-web.vercel.app
   heroku config:set SECRET_KEY=your-production-secret-key
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy ML service"
   git push heroku main
   ```

### Option 4: Google Cloud Run

For more advanced users who want Google Cloud integration.

#### Steps:

1. **Create Dockerfile**

   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       g++ \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Expose port
   EXPOSE 8000

   # Run the application
   CMD ["python", "run.py"]
   ```

2. **Deploy to Cloud Run**
   ```bash
   # Build and deploy
   gcloud run deploy ml-service \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Recommended: Railway Deployment (Step-by-Step)

### 1. Prepare Your Repository

Make sure your `ml-service` directory contains:

- ✅ `requirements.txt`
- ✅ `run.py`
- ✅ `app/` directory with all Python files
- ✅ `cnn_sign_model.h5` (your trained model)

### 2. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will detect the Python app automatically

### 3. Configure Environment Variables

In Railway dashboard, go to Variables tab and add:

```
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
ALLOWED_ORIGINS=https://plp-document-authentication-web.vercel.app,http://localhost:3000
SECRET_KEY=your-super-secret-production-key-here
CONFIDENCE_THRESHOLD=0.75
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

### 4. Update Your Web App

After deployment, update your web app's environment variables:

```
ML_SERVICE_URL=https://your-railway-app.railway.app
```

## Testing Your Deployment

### 1. Check API Health

Visit: `https://your-ml-service-url.com/`
Should return:

```json
{
  "message": "Signature Verification API is running",
  "model_status": "Loaded successfully",
  "model_type": "Real CNN Signature Verification Model"
}
```

### 2. Test API Documentation

Visit: `https://your-ml-service-url.com/docs`
Should show FastAPI Swagger documentation.

### 3. Test from Your Web App

Make sure your web app can reach the ML service by testing signature verification.

## Troubleshooting

### Common Issues:

1. **Model Not Loading**

   - Check if `cnn_sign_model.h5` is in the root directory
   - Verify file size (should be several MB)
   - Check server logs for TensorFlow errors

2. **CORS Errors**

   - Update `ALLOWED_ORIGINS` to include your Vercel domain
   - Make sure there are no trailing slashes

3. **Memory Issues**

   - TensorFlow models can be memory-intensive
   - Consider upgrading to a higher-tier plan if needed

4. **Build Failures**
   - Check if all dependencies in `requirements.txt` are compatible
   - Some packages might need specific versions for deployment

## Cost Considerations

- **Railway**: Free tier available, paid plans start at $5/month
- **Render**: Free tier available, paid plans start at $7/month
- **Heroku**: No free tier, paid plans start at $7/month
- **Google Cloud Run**: Pay-per-use, can be very cost-effective

## Security Notes

1. **Change Default Secret Key**: Use a strong, random secret key in production
2. **Restrict CORS Origins**: Only allow your actual domains
3. **Environment Variables**: Never commit sensitive data to version control
4. **HTTPS**: All production deployments should use HTTPS

## Next Steps

After successful deployment:

1. Update your web app's `ML_SERVICE_URL` environment variable
2. Test the integration between your web app and ML service
3. Monitor the ML service logs for any issues
4. Set up monitoring/alerting if needed
