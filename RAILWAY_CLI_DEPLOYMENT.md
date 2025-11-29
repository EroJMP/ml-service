# Railway CLI Deployment (No GitHub Required)

## 🚀 **Deploy ML Service Using Railway CLI**

### **Step 1: Install Railway CLI**

```bash
npm install -g @railway/cli
```

### **Step 2: Login to Railway**

```bash
railway login
```

- This will open your browser to authenticate with Railway
- Sign up/login with your email or GitHub account

### **Step 3: Navigate to ML Service Directory**

```bash
cd ml-service
```

### **Step 4: Initialize Railway Project**

```bash
railway init
```

- This will create a new Railway project
- You'll be prompted to enter a project name (e.g., `signature-verification-ml`)

### **Step 5: Set Environment Variables**

```bash
railway variables set API_HOST=0.0.0.0
railway variables set API_PORT=8000
railway variables set DEBUG=False
railway variables set ALLOWED_ORIGINS=https://plp-document-authentication-web.vercel.app,http://localhost:3000
railway variables set SECRET_KEY=sk-railway-prod-2024
railway variables set CONFIDENCE_THRESHOLD=0.75
railway variables set SUPABASE_URL=https://joyeyywougvzqdnffzch.supabase.co
railway variables set SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpveWV5eXdvdWd2enFkbmZmemNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5MDgyNDMsImV4cCI6MjA3NDQ4NDI0M30.kerFvoVauTwcGmhYj71jmgnULmgLYXZBYwWrhnQ33G0
railway variables set SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpveWV5eXdvdWd2enFkbmZmemNoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODkwODI0MywiZXhwIjoyMDc0NDg0MjQzfQ.Ymnd1vq5v-NHi50HqwsKC9zIWKHlVWwM5-o-uZTNy3s
```

### **Step 6: Deploy to Railway**

```bash
railway up
```

- This will build and deploy your ML service
- The process may take 5-10 minutes for the first deployment

### **Step 7: Get Your Service URL**

```bash
railway domain
```

- This will show you the URL where your ML service is deployed
- Example: `https://your-app-name.railway.app`

### **Step 8: Test Your Deployment**

1. **Health Check**: Visit `https://your-app-name.railway.app/`
2. **API Docs**: Visit `https://your-app-name.railway.app/docs`

## 🔧 **Useful Railway CLI Commands**

### **View Logs**

```bash
railway logs
```

### **Open in Browser**

```bash
railway open
```

### **Check Status**

```bash
railway status
```

### **View Environment Variables**

```bash
railway variables
```

### **Connect to Service**

```bash
railway connect
```

## 📋 **What You Need Before Deployment**

### **Required Files in ml-service Directory:**

- ✅ `requirements.txt` (with all dependencies)
- ✅ `run.py` (entry point)
- ✅ `app/` directory (with all Python files)
- ✅ `cnn_sign_model.h5` (your trained model)

### **Environment Variables to Set:**

```env
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

## 🎯 **Expected Results**

### **Successful Deployment:**

- ✅ Build completes without errors
- ✅ Service starts successfully
- ✅ Health check returns model status
- ✅ API documentation is accessible

### **Health Check Response:**

```json
{
  "message": "Signature Verification API is running",
  "model_status": "Loaded successfully",
  "model_type": "Real CNN Signature Verification Model",
  "is_mock": false
}
```

## 🚨 **Troubleshooting**

### **Build Fails:**

- Check that all files are in the correct directory
- Verify `requirements.txt` has all dependencies
- Check Railway logs: `railway logs`

### **Model Not Loading:**

- Ensure `cnn_sign_model.h5` is in the root directory
- Check file size (should be several MB)
- Verify model file is not corrupted

### **Service Won't Start:**

- Check environment variables are set correctly
- Verify port configuration
- Check Railway logs for errors

## 🎉 **After Successful Deployment**

1. **Update your web app** with the ML service URL:

   ```
   ML_SERVICE_URL=https://your-app-name.railway.app
   ```

2. **Test the integration** between your web app and ML service

3. **Monitor the service** using Railway dashboard or CLI commands

## 💰 **Cost**

- **Free tier**: 500 hours/month
- **Pro plan**: $5/month for unlimited usage
- **No credit card required** for free tier
