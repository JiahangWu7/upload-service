# app_streamlit.py
# A tiny Streamlit UI to test your FastAPI upload service.
# It talks to POST /upload/image and POST /upload/file and shows JSON responses.

import os
import requests
import streamlit as st
from io import BytesIO
from PIL import Image

# --------------------
# Config
# --------------------
DEFAULT_API_URL = os.getenv("UPLOAD_API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Upload Service Tester", page_icon="⬆️", layout="centered")

st.title("Upload Service Tester ⬆️")
st.caption("FastAPI upload-only service • Image/File endpoints • Simple local tester")

api_url = st.text_input("API Base URL", value=DEFAULT_API_URL, help="Usually http://127.0.0.1:8000")
health_col, _ = st.columns([1, 3])
with health_col:
    if st.button("Check /health"):
        try:
            resp = requests.get(f"{api_url}/health", timeout=10)
            st.success("Service OK!")
            st.json(resp.json())
        except Exception as e:
            st.error(f"Health check failed: {e}")

st.markdown("---")

# --------------------
# Image upload
# --------------------
st.subheader("Upload Image 🖼️")
st.caption("Allowed: jpg, jpeg, png, webp • Size ≤ 20 MB (unless you changed MAX_MB)")

img_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=False,
    key="img_uploader",
)

if img_file is not None:
    # Preview (best-effort)
    try:
        img = Image.open(img_file)
        st.image(img, caption=f"Preview: {img_file.name}", use_container_width=True)
    except Exception:
        st.info("Preview unavailable for this content, but you can still upload.")

if st.button("Send to /upload/image", type="primary", disabled=(img_file is None)):
    if not api_url:
        st.warning("Please set API Base URL")
    else:
        try:
            # reset read pointer
            img_file.seek(0)
            files = {"file": (img_file.name, img_file.read(), img_file.type or "application/octet-stream")}
            with st.spinner("Uploading image..."):
                r = requests.post(f"{api_url}/upload/image", files=files, timeout=60)
            if r.ok:
                st.success("Upload OK")
                st.json(r.json())
            else:
                st.error(f"Upload failed: {r.status_code}")
                try:
                    st.json(r.json())
                except Exception:
                    st.write(r.text)
        except Exception as e:
            st.error(f"Request error: {e}")

st.markdown("---")

# --------------------
# File upload
# --------------------
st.subheader("Upload File 📄")
st.caption("Allowed: txt, pdf, docx, xlsx • Size ≤ 20 MB (unless you changed MAX_MB)")

doc_file = st.file_uploader(
    "Choose a file",
    type=["txt", "pdf", "docx", "xlsx"],
    accept_multiple_files=False,
    key="doc_uploader",
)

if st.button("Send to /upload/file", disabled=(doc_file is None)):
    if not api_url:
        st.warning("Please set API Base URL")
    else:
        try:
            doc_file.seek(0)
            files = {"file": (doc_file.name, doc_file.read(), doc_file.type or "application/octet-stream")}
            with st.spinner("Uploading file..."):
                r = requests.post(f"{api_url}/upload/file", files=files, timeout=120)
            if r.ok:
                st.success("Upload OK")
                st.json(r.json())
            else:
                st.error(f"Upload failed: {r.status_code}")
                try:
                    st.json(r.json())
                except Exception:
                    st.write(r.text)
        except Exception as e:
            st.error(f"Request error: {e}")

st.markdown("---")
st.caption("Tip: change MAX_MB via env var, e.g. `export MAX_MB=50` before starting the FastAPI service.")
