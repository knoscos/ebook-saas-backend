# api/index.py
"""
Root FastAPI app for Ebook SaaS Backend.
This file wires up routes and provides health/readiness endpoints.
Do NOT put your OPENAI_API_KEY here — add it in Vercel env vars.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import routers (these files will be added next)
from api.generate_section import router as generate_router
from api.compile_pdf import router as pdf_router

app = FastAPI(
    title="Ebook SaaS Backend",
    description="Premium ebook generator API (text + images + PDF exports)",
    version="1.0.0",
)

# CORS - allow your Lovable frontend domain(s) here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during development allow all; lock this down to your domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers from other modules
app.include_router(generate_router, prefix="", tags=["generation"])
app.include_router(pdf_router, prefix="", tags=["export"])

# simple health and readiness endpoints
@app.get("/health")
def health():
    return {"status": "ok", "service": "ebook-saas-backend"}

@app.get("/")
def root():
    return {
        "message": "Ebook SaaS Backend is running. Use /generate_section and /compile_pdf endpoints.",
        "version": app.version,
    }
