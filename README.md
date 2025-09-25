# Upload Service 

Hi! This is a super simple **upload-only service** I made.  
It lets you upload **images** or **files** through API calls.  
Right now it only saves the files — no fancy processing (like OCR or recognition) yet.  
But later we can add those features step by step.  

---

## What This Service Does

- ✅ You can upload a **photo** (jpg / jpeg / png / webp).  
- ✅ You can upload a **file** (txt / pdf / docx / xlsx).  
- ✅ It will store them in a local folder (`storage/`).  
- ✅ It gives you back a JSON response with info (id, filename, size, etc).  
- ❌ It does **NOT** analyze the files yet (no OCR, no text extraction). That will be the **next step**.

Basically: **Frontend button → Main backend API → This service → JSON response** 

---

## API Endpoints

### `GET /health`
Just a simple check to see if the service is running.  
Returns status, supported types, and size limit.

---

### `POST /upload/image`
Upload an image. Supports: **jpg, jpeg, png, webp**.  
Returns:
```json
{
  "id": "abc123",
  "kind": "image",
  "filename": "photo.jpg",
  "stored_path": "storage/images/abc123.jpg",
  "size_bytes": 12345,
  "mime_type": "image/jpeg",
  "message": "uploaded"
}
