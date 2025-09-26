# Upload Service

This is a small service I built with **FastAPI**.  
Right now it’s pretty basic, but it already works and can be used by the main backend and the frontend.

---

## What it does

- It has two endpoints:  
  - `/upload/image` → for images  
  - `/upload/file` → for documents  
- Both endpoints check the file type (there is a whitelist) and limit the size to **20 MB**.  
- Uploaded files are saved under the local `storage/` folder, in different sub-directories depending on type.  
- The API returns a JSON response that includes:
  - `id`  
  - `filename`  
  - `stored_path`  
  - `mime_type`  
  - `size_bytes`

This makes it easy for the main backend to save the info into a database, or for the frontend to just show it to users.

---

## Why it’s useful

At this stage there’s **no extra processing** (so no OCR, no text extraction, no image recognition yet).  
The main code can already call this service and get structured results.  
Later on, we can add OCR and recognition step by step without breaking the existing APIs.

---

## Limits

- **Max size**: 20 MB per file  
- **Allowed image types**: `jpg`, `jpeg`, `png`, `webp`  
- **Allowed file types**: `txt`, `pdf`, `docx`, `xlsx`  

---

## How to run

1. Create a virtual environment  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   # .venv\Scripts\Activate.ps1  # Windows PowerShell
   ``` 

2. Install dependencies
  ```bash
  pip install -r requirements.txt
  ``` 

3. Start the service
  ```bash
  uvicorn app.main:app --reload --port 8000
  ``` 

---

## How to test

1. Check health
   ```bash
   curl http://localhost:8000/health
   ``` 


2. Upload an image
  ```bash
  curl -F "file=@photo.jpg" http://localhost:8000/upload/image
  ```

3. Upload a file
  ```bash
  curl -F "file=@doc.pdf" http://localhost:8000/upload/file
  ```

## Optional: Test with Streamlit

For easier testing without using curl, you can run a simple Streamlit UI.

1.Install extra dependencies
```bash
pip install streamlit requests pillow
```

2.Run your FastAPI service (in one terminal)
```bash
uvicorn app.main:app --reload --port 8000
```

3.In another terminal, start Streamlit (from the project root)
```bash
streamlit run app_streamlit.py
```

4.Open the page (usually http://localhost:8501
) and:

* Click Check /health to confirm the service is alive

* Upload an image (→ calls /upload/image)

* Upload a file (→ calls /upload/file)

The JSON response will be shown directly in the page.



