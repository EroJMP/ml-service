# Railway Deployment - Step by Step

## 🚀 **Railway Deployment for ML Service**

### **Step 1: Create Railway Account**

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign up with your GitHub account

### **Step 2: Deploy from GitHub**

1. Click **"Deploy from GitHub repo"**
2. Select your repository: `capstone-final`
3. Railway will detect it's a Python project

### **Step 3: Configure the Project**

1. **Set Root Directory**:

   - Click on your project
   - Go to **Settings** → **Root Directory**
   - Set to: `ml-service`

2. **Set Start Command**:
   - Go to **Settings** → **Deploy**
   - Set start command: `python run.py`

### **Step 4: Set Environment Variables**

Go to **Variables** tab and add:

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

### **Step 5: Deploy**

1. Railway will automatically build and deploy
2. Wait for the build to complete (5-10 minutes)
3. Your ML service will be available at: `https://your-app-name.railway.app`

### **Step 6: Test Your Deployment**

1. **Health Check**: Visit `https://your-app-name.railway.app/`
2. **API Docs**: Visit `https://your-app-name.railway.app/docs`
3. **Test Endpoint**: Try the signature verification endpoints

### **Step 7: Update Your Web App**

In your Vercel project, add this environment variable:

```
ML_SERVICE_URL=https://your-app-name.railway.app
```

## 🎯 **What You'll Get**

### **✅ Full ML Functionality**

- Real TensorFlow model loading
- Actual signature verification
- OpenCV image processing
- Complete API functionality

### **✅ Production Ready**

- HTTPS enabled
- Auto-scaling
- Health monitoring
- Logs and metrics

### **✅ Cost Effective**

- Free tier: 500 hours/month
- Pro plan: $5/month for unlimited

## 🔧 **Troubleshooting**

### **Build Fails**

- Check that `cnn_sign_model.h5` is in the `ml-service` directory
- Verify all dependencies in `requirements.txt`

### **Model Not Loading**

- Check the logs in Railway dashboard
- Verify the model file is not corrupted

### **CORS Errors**

- Update `ALLOWED_ORIGINS` to include your Vercel domain
- Make sure there are no trailing slashes

## 📊 **Expected Response**

When you visit the health check endpoint, you should see:

```json
{
  "message": "Signature Verification API is running",
  "model_status": "Loaded successfully",
  "model_type": "Real CNN Signature Verification Model",
  "is_mock": false
}
```

## 🎉 **Success!**

Once deployed, your ML service will provide real signature verification capabilities to your web application!
