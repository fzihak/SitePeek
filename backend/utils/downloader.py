import requests
from typing import Tuple

class FileDownloader:
    """Download files from URLs with proper content type handling."""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the downloader.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def download_file(self, url: str) -> Tuple[bytes, str]:
        """
        Download a file from a URL.
        
        Args:
            url: The URL of the file to download
            
        Returns:
            Tuple of (file_content as bytes, content_type as string)
            
        Raises:
            Exception: If the download fails
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Get content type from response headers
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            
            return response.content, content_type
            
        except requests.exceptions.Timeout:
            raise Exception(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to download file: {str(e)}")
    
    def get_content_type(self, url: str) -> str:
        """
        Get the content type of a file without downloading it.
        
        Args:
            url: The URL of the file
            
        Returns:
            Content type string
        """
        try:
            response = requests.head(url, headers=self.headers, timeout=self.timeout)
            return response.headers.get('Content-Type', 'application/octet-stream')
        except Exception:
            # Fallback to guessing from extension
            return self._guess_content_type(url)
    
    def _guess_content_type(self, url: str) -> str:
        """
        Guess content type from file extension.
        
        Args:
            url: The URL of the file
            
        Returns:
            Guessed content type string
        """
        extension_map = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.webp': 'image/webp',
            '.ico': 'image/x-icon',
            '.pdf': 'application/pdf',
            '.zip': 'application/zip',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2',
            '.ttf': 'font/ttf',
            '.eot': 'application/vnd.ms-fontobject',
            '.otf': 'font/otf',
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
        }
        
        url_lower = url.lower()
        for ext, content_type in extension_map.items():
            if url_lower.endswith(ext):
                return content_type
        
        return 'application/octet-stream'