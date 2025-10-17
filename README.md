# SitePeek — A WebSource Analyzer

**Developed by Foysal Zihak**

A modern, production-ready web application that analyzes any public website URL and displays detailed information about its source code, assets, fonts, colors, and file structure.

![SitePeek](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal.svg)

## ✨ Features

- **Source Code Analysis**: View and download complete HTML source code
- **Asset Extraction**: Automatically detect and list all CSS, JavaScript, images, and other files
- **Color Palette**: Extract and display all colors used in the website
- **Font Detection**: Identify all font families used across the site
- **File Structure**: Visual tree representation of website file organization
- **Individual Downloads**: Download any file with a single click
- **Bulk Download**: Download all assets as a ZIP archive
- **Responsive Design**: Beautiful UI that works on all devices
- **Real-time Analysis**: Fast processing with loading animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or download the project**

```bash
cd SitePeek
```

2. **Set up the backend**

```bash
cd backend
pip install -r requirements.txt
```

3. **Start the backend server**

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

4. **Open the frontend**

```bash
cd ../frontend
```

Simply open `index.html` in your browser, or use a local server:

```bash
# Using Python's built-in server
python -m http.server 3000

# Or using Node.js http-server (if installed)
npx http-server -p 3000
```

Visit `http://localhost:3000` in your browser.

## 📁 Project Structure

```
SitePeek/
├── backend/
│   ├── main.py              # FastAPI application and endpoints
│   ├── requirements.txt     # Python dependencies
│   └── utils/
│       ├── extractor.py     # Website content extraction logic
│       └── downloader.py    # File download utilities
├── frontend/
│   ├── index.html          # Main HTML structure
│   ├── style.css           # Styling and responsive design
│   └── script.js           # Frontend logic and API calls
└── README.md               # This file
```

## 🔧 API Endpoints

### `POST /analyze`

Analyze a website and extract all information.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "html_source": "<!DOCTYPE html>...",
  "css_files": ["https://example.com/style.css"],
  "js_files": ["https://example.com/script.js"],
  "images": ["https://example.com/logo.png"],
  "others": ["https://example.com/font.woff2"],
  "colors": ["#3B82F6", "rgb(255, 255, 255)"],
  "fonts": ["Inter", "Arial"],
  "structure": {...},
  "summary": {
    "total_css": 5,
    "total_js": 10,
    "total_images": 20,
    "total_others": 3
  }
}
```

### `GET /download`

Download a single file.

**Query Parameters:**
- `file_url`: The URL of the file to download

**Response:** File stream with appropriate content type

### `POST /download-all`

Download all assets as a ZIP file.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:** ZIP file stream

### `GET /`

Health check endpoint.

## 🎨 Features in Detail

### Source Code Analysis
- View the complete HTML source code
- Syntax-friendly preview with truncation
- Download as `.html` file
- Modal view for full source inspection

### Asset Detection
- **CSS Files**: All linked stylesheets and imported styles
- **JavaScript Files**: All script sources
- **Images**: JPG, PNG, GIF, SVG, WebP, and more
- **Other Files**: Fonts, PDFs, videos, documents

### Color Extraction
- Detects HEX, RGB, RGBA, and HSL colors
- Visual color swatches
- Removes duplicates automatically
- Displays up to 24 unique colors

### Font Analysis
- Extracts font-family declarations
- Identifies @font-face definitions
- Live font preview with sample text
- Handles multiple font formats

### File Structure Tree
- Hierarchical visualization of file paths
- Folder and file differentiation
- Clean, readable tree format

### Download Capabilities
- Individual file downloads with preserved names
- Bulk ZIP download (limits: 20 CSS, 20 JS, 30 images)
- Progress indication for ZIP creation
- Error handling for failed downloads

## 🛠️ Configuration

### Backend Configuration

Edit `backend/main.py` to modify:

- **CORS settings**: Update `allow_origins` for production
- **Timeout values**: Adjust request timeouts in extractor
- **Download limits**: Modify file count limits in ZIP creation

### Frontend Configuration

Edit `frontend/script.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Change for production
```

## 🔒 Security Considerations

- The application only analyzes publicly accessible websites
- CORS is configured for development (`allow_origins=["*"]`)
- For production, restrict CORS to your frontend domain
- Consider adding rate limiting for API endpoints
- Implement authentication if deploying publicly

## 🐛 Troubleshooting

### Backend won't start

- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available

### CORS errors

- Verify backend is running on `http://localhost:8000`
- Check `API_BASE_URL` in `script.js` matches backend
- Ensure CORS middleware is properly configured

### Analysis fails

- Verify the target website is publicly accessible
- Check internet connection
- Some websites block automated requests (rate limiting)
- Try with a different website

### Files won't download

- Check browser console for errors
- Verify backend `/download` endpoint is accessible
- Some file URLs may require authentication

## 📝 Development

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Extraction Logic**: Extend `extractor.py` with new parsers
3. **Frontend**: Update UI in `index.html` and logic in `script.js`

### Testing

Test the API using curl:

```bash
# Test analyze endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

# Test download endpoint
curl "http://localhost:8000/download?file_url=https://example.com/style.css" \
  --output test.css
```

## 🚀 Deployment

### Backend Deployment (Production)

1. Update CORS settings in `main.py`
2. Set environment variables
3. Use a production ASGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

4. Deploy to platforms like:
   - Heroku
   - AWS EC2
   - DigitalOcean
   - Railway
   - Render

### Frontend Deployment

Deploy static files to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

Update `API_BASE_URL` to your production backend URL.

## 📄 License

This project is created for educational and professional use.

## 👤 Author

**Foysal Zihak**

## 🙏 Acknowledgments

- Built with FastAPI and vanilla JavaScript
- UI inspired by modern design systems (Vercel, shadcn/ui)
- Icons from Feather Icons concept

## 📞 Support

For issues or questions, please check:
1. This README
2. Code comments in source files
3. FastAPI documentation: https://fastapi.tiangolo.com/

---

**Made with ❤️ by Foysal Zihak**