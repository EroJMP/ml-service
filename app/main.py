from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, cast, Any
import numpy as np
import cv2
import io
from PIL import Image
import os
import uuid
import sys
import traceback
from datetime import datetime
from pydantic import BaseModel
import shutil
import base64

# Try to import TensorFlow, use mock if not available
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("WARNING: TensorFlow not available, using mock model for development")
    tf = None
    TENSORFLOW_AVAILABLE = False

# Import config and database
from app.config import ALLOWED_ORIGINS, MODEL_PATH, UPLOAD_DIR, DB_DIR, CONFIDENCE_THRESHOLD

from app.database import signature_sets_db

# Initialize FastAPI app
app = FastAPI(
    title="Signature Verification API",
    description="API for verifying signatures using CNN model",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the CNN model
model = None
use_mock_model = False

if TENSORFLOW_AVAILABLE:
    try:
        print(f"Attempting to load model from: {MODEL_PATH}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Model file exists: {os.path.exists(MODEL_PATH)}")
        
        # Load the model with TensorFlow
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        
        # Compile the model
        if model is not None:
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
            model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
            
            print(f"Model loaded successfully from {MODEL_PATH}")
            
            # Print model summary
            if hasattr(model, 'summary'):
                model.summary()
    except Exception as e:
        print(f"ERROR loading TensorFlow model: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        model = None
        use_mock_model = False
else:
    print("TensorFlow not available, loading mock model...")
    model = None

# If no real model loaded, try mock model
if model is None:
    try:
        from app.mock_model import load_mock_model
        model = load_mock_model()
        use_mock_model = True
        print("SUCCESS: Mock model loaded for development/testing")
        print("WARNING: This is not the real CNN model. Install TensorFlow for production use.")
    except Exception as mock_error:
        print(f"ERROR loading mock model: {mock_error}")
        model = None

# Pydantic models for request/response
class SignatureVerificationResult(BaseModel):
    filename: str
    is_authentic: bool
    confidence: float

class SignatureSetResult(BaseModel):
    id: str
    date_uploaded: str
    signatures: List[SignatureVerificationResult]
    all_authentic: bool

class SignatureSetResponse(BaseModel):
    id: str
    date_uploaded: str
    all_authentic: bool
    signature_count: int

class Base64SignatureRequest(BaseModel):
    signatures: List[str]  # Base64 encoded images
    user_id: str
    signature_type: str  # 'student' or 'parent'

class SignatureVerificationResponse(BaseModel):
    verification_id: str
    results: List[SignatureVerificationResult]
    all_authentic: bool
    flagged_indices: List[int]  # Indices of signatures that are flagged as forge

def preprocess_image(image_bytes):
    """
    Preprocess the image for the CNN model using the approach from main.py.
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL image to numpy array
        cur_img = np.array(img)
        
        # Preprocess the image for the model
        cur_img = cv2.cvtColor(cur_img, cv2.COLOR_BGR2RGB)
        cur_img = cv2.resize(cur_img, (224, 224))
        cur_img = cur_img.astype('float32') / 255.0
        cur_img = cur_img.reshape((1, 224, 224, 3))
        
        return cur_img
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def preprocess_base64_image(base64_string):
    """
    Preprocess a base64 encoded image for the CNN model.
    """
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(base64_string)
        
        # Use existing preprocess_image function
        return preprocess_image(image_bytes)
    
    except Exception as e:
        print(f"Error preprocessing base64 image: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=f"Error processing base64 image: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint for Railway deployment."""
    try:
        if model is None:
            return {
                "message": "Signature Verification API is running",
                "model_status": "NOT LOADED - Check server logs",
                "model_path": MODEL_PATH,
                "model_exists": os.path.exists(MODEL_PATH),
                "error": "No model available",
                "status": "unhealthy"
            }
        
        model_type = "Mock CNN Model (Development)" if use_mock_model else "Real CNN Signature Verification Model"
        
        return {
            "message": "Signature Verification API is running",
            "model_status": "Loaded successfully",
            "model_type": model_type,
            "is_mock": use_mock_model,
            "warning": "Using mock model - install TensorFlow for production" if use_mock_model else None,
            "status": "healthy"
        }
    except Exception as e:
        return {
            "message": "Signature Verification API is running",
            "model_status": "Error during health check",
            "error": str(e),
            "status": "unhealthy"
        }

@app.get("/health")
async def health_check():
    """Simple health check endpoint for Railway."""
    return {"status": "healthy", "message": "Service is running"}

@app.post("/verify-signature", response_model=SignatureVerificationResult)
async def verify_single_signature(file: UploadFile = File(...)):
    """Verify a single signature image."""
    if not model:
        raise HTTPException(
            status_code=500, 
            detail="Model not loaded. Please check server logs for details."
        )
    
    # Read file content
    contents = await file.read()
    
    # Preprocess the image
    img_array = preprocess_image(contents)
    
    # Make prediction
    try:
        prediction = model.predict(img_array)
        
        # Get the index of the maximum value
        a = np.argmax(prediction, axis=1)
        
        # Get confidence percentage for real signature (assuming index 0 is real)
        real_confidence = float(prediction[0][0])
        
        # Apply threshold - if confidence for real signature is >= CONFIDENCE_THRESHOLD, mark as authentic
        is_authentic = real_confidence >= CONFIDENCE_THRESHOLD
        
        # Use the confidence for the predicted class
        confidence = real_confidence if is_authentic else (1.0 - real_confidence)
        
        return SignatureVerificationResult(
            filename=file.filename or "unknown",
            is_authentic=is_authentic,
            confidence=confidence
        )
    except Exception as e:
        print(f"Error during prediction: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

@app.post("/verify-signature-set", response_model=SignatureSetResult)
async def verify_signature_set(files: List[UploadFile] = File(...)):
    """Verify a set of signatures (7 required)."""
    if not model:
        raise HTTPException(
            status_code=500, 
            detail="Model not loaded. Please check server logs for details."
        )
    
    if len(files) != 7:
        raise HTTPException(status_code=400, detail="Exactly 7 signature files are required")
    
    set_id = str(uuid.uuid4())
    set_dir = os.path.join(UPLOAD_DIR, set_id)
    os.makedirs(set_dir, exist_ok=True)
    
    results = []
    all_authentic = True
    
    for file in files:
        # Read file content
        contents = await file.read()
        
        # Save file
        file_path = os.path.join(set_dir, file.filename or f"file-{uuid.uuid4()}.jpg")
        with open(file_path, "wb") as f:
            # Reset file pointer to beginning
            await file.seek(0)
            # Write file content
            shutil.copyfileobj(file.file, f)
        
        # Preprocess the image
        img_array = preprocess_image(contents)
        
        try:
            # Make prediction
            prediction = model.predict(img_array)
            
            # Get confidence percentage for real signature (assuming index 0 is real)
            real_confidence = float(prediction[0][0])
            
            # Apply threshold - if confidence for real signature is >= CONFIDENCE_THRESHOLD, mark as authentic
            is_authentic = real_confidence >= CONFIDENCE_THRESHOLD
            
            # Use the confidence for the predicted class
            confidence = real_confidence if is_authentic else (1.0 - real_confidence)
            
            if not is_authentic:
                all_authentic = False
            
            results.append(
                SignatureVerificationResult(
                    filename=file.filename or f"file-{uuid.uuid4()}.jpg",
                    is_authentic=is_authentic,
                    confidence=confidence
                )
            )
        except Exception as e:
            print(f"Error during prediction for file {file.filename}: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")
    
    # Save the results
    signature_set = SignatureSetResult(
        id=set_id,
        date_uploaded=datetime.now().isoformat(),
        signatures=results,
        all_authentic=all_authentic
    )
    
    # Save to our database
    signature_sets_db.create(set_id, signature_set.dict())
    
    return signature_set

@app.get("/signature-sets", response_model=List[SignatureSetResponse])
async def get_signature_sets():
    """Get all signature sets."""
    all_sets = signature_sets_db.get_all()
    
    return [
        SignatureSetResponse(
            id=set_id,
            date_uploaded=set_data["date_uploaded"],
            all_authentic=set_data["all_authentic"],
            signature_count=len(set_data["signatures"])
        )
        for set_id, set_data in all_sets.items()
    ]

@app.get("/signature-set/{set_id}", response_model=SignatureSetResult)
async def get_signature_set(set_id: str):
    """Get details of a specific signature set."""
    set_data = signature_sets_db.get(set_id)
    if not set_data:
        raise HTTPException(status_code=404, detail="Signature set not found")
    
    return set_data

@app.delete("/signature-set/{set_id}")
async def delete_signature_set(set_id: str):
    """Delete a signature set."""
    set_data = signature_sets_db.get(set_id)
    if not set_data:
        raise HTTPException(status_code=404, detail="Signature set not found")
    
    # Remove from database
    signature_sets_db.delete(set_id)
    
    # Remove files
    set_dir = os.path.join(UPLOAD_DIR, set_id)
    if os.path.exists(set_dir):
        shutil.rmtree(set_dir)
    
    return {"message": "Signature set deleted successfully"}

@app.post("/verify-student-signatures", response_model=SignatureVerificationResponse)
async def verify_student_signatures(request: Base64SignatureRequest):
    """
    Verify signatures from the student portal.
    This endpoint accepts base64 encoded signatures and returns verification results.
    """
    if not model:
        raise HTTPException(
            status_code=500, 
            detail="Model not loaded. Please check server logs for details."
        )
    
    if len(request.signatures) == 0:
        raise HTTPException(status_code=400, detail="At least one signature is required")
    
    if len(request.signatures) > 7:
        raise HTTPException(status_code=400, detail="Maximum 7 signatures allowed")
    
    verification_id = str(uuid.uuid4())
    results = []
    flagged_indices = []
    all_authentic = True
    
    for i, base64_signature in enumerate(request.signatures):
        try:
            # Preprocess the base64 image
            img_array = preprocess_base64_image(base64_signature)
            
            # Make prediction
            prediction = model.predict(img_array)
            
            # Get confidence percentage for real signature (assuming index 0 is real)
            real_confidence = float(prediction[0][0])
            
            # Apply threshold - if confidence for real signature is >= CONFIDENCE_THRESHOLD, mark as authentic
            is_authentic = real_confidence >= CONFIDENCE_THRESHOLD
            
            # Use the confidence for the predicted class
            confidence = real_confidence if is_authentic else (1.0 - real_confidence)
            
            if not is_authentic:
                all_authentic = False
                flagged_indices.append(i)
            
            results.append(
                SignatureVerificationResult(
                    filename=f"signature_{i+1}",
                    is_authentic=is_authentic,
                    confidence=confidence
                )
            )
            
        except Exception as e:
            print(f"Error during prediction for signature {i+1}: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=f"Error during prediction for signature {i+1}: {str(e)}")
    
    # Create verification response
    verification_response = SignatureVerificationResponse(
        verification_id=verification_id,
        results=results,
        all_authentic=all_authentic,
        flagged_indices=flagged_indices
    )
    
    # Store the verification result for potential future reference
    verification_data = {
        "user_id": request.user_id,
        "signature_type": request.signature_type,
        "verification_id": verification_id,
        "date_verified": datetime.now().isoformat(),
        "results": [result.dict() for result in results],
        "all_authentic": all_authentic,
        "flagged_indices": flagged_indices
    }
    
    # Save to our database
    signature_sets_db.create(f"verification_{verification_id}", verification_data)
    
    return verification_response


class SingleSignatureRequest(BaseModel):
    signature: str
    threshold: float = 0.9

@app.post("/verify-single-signature")
async def verify_single_signature(request: SingleSignatureRequest):
    """
    Verify a single signature with a specified threshold
    """
    try:
        signature_data = request.signature
        threshold = request.threshold
        
        if not signature_data:
            raise HTTPException(status_code=400, detail="Signature data is required")
        
        print(f"🔍 Verifying single signature with {threshold*100}% threshold...")
        
        # Preprocess the signature
        img_array = preprocess_base64_image(signature_data)
        
        # Get prediction from model
        prediction = model.predict(img_array)
        
        # Extract confidence (assuming index 0 is authentic, index 1 is forge)
        authentic_confidence = float(prediction[0][0])
        forge_confidence = float(prediction[0][1])
        
        # Determine if authentic based on threshold
        is_authentic = authentic_confidence >= threshold
        
        result = {
            "is_authentic": is_authentic,
            "confidence": authentic_confidence,
            "threshold_used": threshold,
            "authentic_confidence": authentic_confidence,
            "forge_confidence": forge_confidence
        }
        
        print(f"✅ Single signature verification result: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in single signature verification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}") 