# Signature Verification ML Service

This FastAPI application provides an API for verifying signatures using a CNN model. It's integrated with the student portal for real-time signature verification.

## Setup

1. **Install dependencies**

```bash
cd ml-service
pip install -r requirements.txt
```

2. **Environment Configuration**

Create a `.env` file in the ml-service directory with the following configuration:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Settings - Allow Next.js app
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Model Settings
CONFIDENCE_THRESHOLD=0.75

# Supabase Configuration (add your actual values)
SUPABASE_URL=your-supabase-url-here
SUPABASE_ANON_KEY=your-supabase-anon-key-here
SUPABASE_SERVICE_KEY=your-supabase-service-key-here
```

3. **Place your CNN model**

Ensure your trained CNN model file `cnn_sign_model.h5` is in the root directory of the ml-service project.

## Running the API

Run the FastAPI application:

```bash
python run.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Core Verification Endpoints

- `GET /`: Check if the API is running and model status
- `POST /verify-signature`: Verify a single signature image (file upload)
- `POST /verify-signature-set`: Verify a set of 7 signature images (file upload)
- `POST /verify-student-signatures`: **NEW** - Verify signatures from student portal (base64 encoded)

### Management Endpoints

- `GET /signature-sets`: Get all signature sets
- `GET /signature-set/{set_id}`: Get details of a specific signature set
- `DELETE /signature-set/{set_id}`: Delete a signature set

## Student Portal Integration

The API is integrated with the student portal signature management system:

### Workflow:

1. Student uploads 7 signatures in the signature management tab
2. Student clicks "Verify Signatures" button
3. Signatures are sent to `/verify-student-signatures` endpoint as base64 data
4. ML model analyzes each signature and returns verification results
5. Flagged signatures are highlighted in the UI
6. Student can re-upload flagged signatures until all are verified as authentic
7. Verified signatures are saved to permanent storage

### Frontend Integration

- Student Portal: `web/src/components/settings/SignatureUploadModal.tsx`
- API Route: `web/src/app/api/verify-signatures/route.ts` (to be created)

## Requirements

- Python 3.8+
- TensorFlow 2.13+
- FastAPI 0.104+
- Other dependencies listed in requirements.txt
