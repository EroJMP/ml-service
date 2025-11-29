# Render Deployment (No GitHub Required)

## 🚀 **Deploy ML Service to Render**

### **Step 1: Create Render Account**

1. Go to [render.com](https://render.com)
2. Sign up with your email (no GitHub required)
3. Verify your email address

### **Step 2: Create New Web Service**

1. Click **"New +"** button
2. Select **"Web Service"**
3. Choose **"Build and deploy from a Git repository"** or **"Deploy without Git"**

### **Step 3: Deploy Without Git (Manual Upload)**

1. Select **"Deploy without Git"**
2. **Upload your files**:
   - Create a ZIP file of your `ml-service` directory
   - Upload the ZIP file to Render
3. **Configure the service**:
   - **Name**: `signature-verification-ml`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`

### **Step 4: Set Environment Variables**

In the Render dashboard, go to **Environment** tab and add:

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

1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes)
3. Your service will be available at: `https://your-app-name.onrender.com`

## 🎯 **Render CLI Alternative**

### **Install Render CLI**

```bash
npm install -g @render/cli
```

### **Login to Render**

```bash
render login
```

### **Deploy from Local Directory**

```bash
cd ml-service
render deploy
```

## 📋 **Render Configuration**

### **Required Files:**

- ✅ `requirements.txt`
- ✅ `run.py`
- ✅ `app/` directory
- ✅ `cnn_sign_model.h5`

### **Render will automatically:**

- ✅ Detect Python runtime
- ✅ Install dependencies from `requirements.txt`
- ✅ Start the service with `python run.py`
- ✅ Provide HTTPS URL

## 💰 **Render Pricing**

- **Free tier**: Available with limitations
- **Starter plan**: $7/month
- **No credit card required** for free tier

## 🎉 **Expected Results**

### **Successful Deployment:**

- ✅ Build completes successfully
- ✅ Service starts and responds to requests
- ✅ Health check endpoint works
- ✅ API documentation accessible

### **Health Check Response:**

```json
{
  "message": "Signature Verification API is running",
  "model_status": "Loaded successfully",
  "model_type": "Real CNN Signature Verification Model"
}
```
