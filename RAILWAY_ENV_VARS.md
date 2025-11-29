# Railway Environment Variables Setup

## 🔧 **Updated Environment Variables for Railway**

Go to your Railway project dashboard → Variables tab and set these:

### **Required Variables:**

```
API_HOST=0.0.0.0
API_PORT=$PORT
DEBUG=False
ALLOWED_ORIGINS=https://plp-document-authentication-web.vercel.app,http://localhost:3000
SECRET_KEY=sk-railway-prod-2024
CONFIDENCE_THRESHOLD=0.75
SUPABASE_URL=https://joyeyywougvzqdnffzch.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpveWV5eXdvdWd2enFkbmZmemNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5MDgyNDMsImV4cCI6MjA3NDQ4NDI0M30.kerFvoVauTwcGmhYj71jmgnULmgLYXZBYwWrhnQ33G0
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpveWV5eXdvdWd2enFkbmZmemNoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODkwODI0MywiZXhwIjoyMDc0NDg0MjQzfQ.Ymnd1vq5v-NHi50HqwsKC9zIWKHlVWwM5-o-uZTNy3s
```

## ⚠️ **Important Changes:**

1. **API_PORT=$PORT** - Railway automatically sets the PORT environment variable
2. **DEBUG=False** - Disable debug mode for production
3. **API_HOST=0.0.0.0** - Allow external connections

## 🚀 **After Setting Variables:**

1. **Redeploy your service** in Railway
2. **Check the logs** to see if it starts properly
3. **Test the health check** endpoint

## 🔍 **What the Updated run.py Does:**

- ✅ **Uses Railway's PORT variable** automatically
- ✅ **Falls back to port 8000** if PORT is not set
- ✅ **Prints the port** for debugging
- ✅ **Handles Railway's deployment requirements**

## 📋 **Expected Log Output:**

When the service starts, you should see:

```
Starting server on port 8080
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

## 🎯 **Next Steps:**

1. **Update the environment variables** in Railway dashboard
2. **Redeploy the service**
3. **Check the logs** for any startup errors
4. **Test the health check** endpoint
