from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel, HttpUrl
import io
import zipfile
from typing import List, Dict, Any
from utils.extractor import WebsiteExtractor
from utils.downloader import FileDownloader

app = FastAPI(title="SitePeek API", version="1.0.0")

# CORS middleware for frontend connection
# Update these origins when deploying to production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",  # Allow all Vercel deployments
        # Add your custom domain here when ready:
        # "https://sitepeek.yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AnalyzeRequest(BaseModel):
    url: HttpUrl

class AnalyzeResponse(BaseModel):
    html_source: str
    css_files: List[str]
    js_files: List[str]
    images: List[str]
    others: List[str]
    colors: List[str]
    fonts: List[str]
    structure: Dict[str, Any]
    summary: Dict[str, int]

class DownloadAllRequest(BaseModel):
    url: HttpUrl

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "SitePeek API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    """
    Analyze a website and return detailed information about its source code,
    assets, fonts, colors, and structure.
    
    Args:
        request: AnalyzeRequest containing the URL to analyze
        
    Returns:
        AnalyzeResponse with all extracted data
        
    Raises:
        HTTPException: If the URL is invalid or cannot be fetched
    """
    try:
        url = str(request.url)
        extractor = WebsiteExtractor(url)
        
        # Fetch and parse the website
        html_source = extractor.fetch_html()
        
        # Extract all resources
        css_files = extractor.extract_css_files()
        js_files = extractor.extract_js_files()
        images = extractor.extract_images()
        others = extractor.extract_other_files()
        
        # Extract design elements
        colors = extractor.extract_colors()
        fonts = extractor.extract_fonts()
        
        # Build file structure
        structure = extractor.build_file_structure(
            css_files + js_files + images + others
        )
        
        # Calculate summary
        summary = {
            "total_css": len(css_files),
            "total_js": len(js_files),
            "total_images": len(images),
            "total_others": len(others)
        }
        
        return AnalyzeResponse(
            html_source=html_source,
            css_files=css_files,
            js_files=js_files,
            images=images,
            others=others,
            colors=colors,
            fonts=fonts,
            structure=structure,
            summary=summary
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Failed to connect to website: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/download")
async def download_file(file_url: str):
    """
    Download a single file from the analyzed website.
    
    Args:
        file_url: The URL of the file to download
        
    Returns:
        StreamingResponse with the file content
        
    Raises:
        HTTPException: If the file cannot be downloaded
    """
    try:
        downloader = FileDownloader()
        file_content, content_type = downloader.download_file(file_url)
        
        # Extract filename from URL
        filename = file_url.split('/')[-1].split('?')[0] or 'file'
        
        return StreamingResponse(
            io.BytesIO(file_content),
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")

@app.post("/download-all")
async def download_all_files(request: DownloadAllRequest):
    """
    Download all files from the analyzed website as a ZIP archive.
    
    Args:
        request: DownloadAllRequest containing the URL
        
    Returns:
        StreamingResponse with the ZIP file
        
    Raises:
        HTTPException: If files cannot be downloaded or zipped
    """
    try:
        url = str(request.url)
        extractor = WebsiteExtractor(url)
        downloader = FileDownloader()
        
        # Fetch HTML source
        html_source = extractor.fetch_html()
        
        # Extract all resource URLs
        css_files = extractor.extract_css_files()
        js_files = extractor.extract_js_files()
        images = extractor.extract_images()
        others = extractor.extract_other_files()
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add HTML source
            zip_file.writestr('index.html', html_source)
            
            # Add CSS files
            for css_url in css_files[:20]:  # Limit to prevent huge downloads
                try:
                    content, _ = downloader.download_file(css_url)
                    filename = css_url.split('/')[-1].split('?')[0] or 'style.css'
                    zip_file.writestr(f'css/{filename}', content)
                except Exception as e:
                    print(f"Failed to download {css_url}: {e}")
            
            # Add JS files
            for js_url in js_files[:20]:
                try:
                    content, _ = downloader.download_file(js_url)
                    filename = js_url.split('/')[-1].split('?')[0] or 'script.js'
                    zip_file.writestr(f'js/{filename}', content)
                except Exception as e:
                    print(f"Failed to download {js_url}: {e}")
            
            # Add images
            for img_url in images[:30]:
                try:
                    content, _ = downloader.download_file(img_url)
                    filename = img_url.split('/')[-1].split('?')[0] or 'image.jpg'
                    zip_file.writestr(f'images/{filename}', content)
                except Exception as e:
                    print(f"Failed to download {img_url}: {e}")
            
            # Add other files
            for other_url in others[:10]:
                try:
                    content, _ = downloader.download_file(other_url)
                    filename = other_url.split('/')[-1].split('?')[0] or 'file'
                    zip_file.writestr(f'others/{filename}', content)
                except Exception as e:
                    print(f"Failed to download {other_url}: {e}")
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=website_assets.zip"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create ZIP: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)