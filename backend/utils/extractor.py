import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Any, Set

class WebsiteExtractor:
    """Extract and analyze website source code, assets, and design elements."""
    
    def __init__(self, url: str, timeout: int = 30):
        """
        Initialize the extractor with a target URL.
        
        Args:
            url: The website URL to analyze
            timeout: Request timeout in seconds
        """
        self.url = url
        self.timeout = timeout
        self.soup = None
        self.html_content = None
        self.base_url = self._get_base_url()
        
    def _get_base_url(self) -> str:
        """Extract the base URL from the full URL."""
        parsed = urlparse(self.url)
        return f"{parsed.scheme}://{parsed.netloc}"
    
    def fetch_html(self) -> str:
        """
        Fetch HTML content from the target URL.
        
        Returns:
            Raw HTML source code as string
            
        Raises:
            ConnectionError: If the request fails
            ValueError: If the URL is invalid
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            self.html_content = response.text
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
            
            return self.html_content
            
        except requests.exceptions.Timeout:
            raise ConnectionError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch URL: {str(e)}")
    
    def extract_css_files(self) -> List[str]:
        """
        Extract all CSS file URLs from the HTML.
        
        Returns:
            List of absolute CSS file URLs
        """
        if not self.soup:
            return []
        
        css_files = []
        
        # Find all <link> tags with rel="stylesheet"
        for link in self.soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(self.url, href)
                css_files.append(absolute_url)
        
        # Find inline <style> imports
        for style in self.soup.find_all('style'):
            style_content = style.string or ''
            imports = re.findall(r'@import\s+["\']([^"\']+)["\']', style_content)
            for imp in imports:
                absolute_url = urljoin(self.url, imp)
                css_files.append(absolute_url)
        
        return list(set(css_files))  # Remove duplicates
    
    def extract_js_files(self) -> List[str]:
        """
        Extract all JavaScript file URLs from the HTML.
        
        Returns:
            List of absolute JavaScript file URLs
        """
        if not self.soup:
            return []
        
        js_files = []
        
        # Find all <script> tags with src attribute
        for script in self.soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                absolute_url = urljoin(self.url, src)
                js_files.append(absolute_url)
        
        return list(set(js_files))  # Remove duplicates
    
    def extract_images(self) -> List[str]:
        """
        Extract all image URLs from the HTML.
        
        Returns:
            List of absolute image URLs
        """
        if not self.soup:
            return []
        
        images = []
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico', '.bmp')
        
        # Find all <img> tags
        for img in self.soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                absolute_url = urljoin(self.url, src)
                images.append(absolute_url)
        
        # Find images in srcset attribute
        for img in self.soup.find_all('img', srcset=True):
            srcset = img.get('srcset', '')
            urls = re.findall(r'(https?://[^\s,]+)', srcset)
            for url in urls:
                images.append(url)
        
        # Find images in picture > source elements
        for source in self.soup.find_all('source', srcset=True):
            srcset = source.get('srcset', '')
            urls = re.findall(r'([^\s,]+)', srcset)
            for url in urls:
                absolute_url = urljoin(self.url, url.split()[0])
                if any(absolute_url.lower().endswith(ext) for ext in image_extensions):
                    images.append(absolute_url)
        
        # Find background images in inline styles
        for element in self.soup.find_all(style=True):
            style = element.get('style', '')
            bg_images = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style)
            for bg_img in bg_images:
                absolute_url = urljoin(self.url, bg_img)
                if any(absolute_url.lower().endswith(ext) for ext in image_extensions):
                    images.append(absolute_url)
        
        return list(set(images))  # Remove duplicates
    
    def extract_other_files(self) -> List[str]:
        """
        Extract other file types (fonts, PDFs, videos, etc.).
        
        Returns:
            List of absolute URLs for other file types
        """
        if not self.soup:
            return []
        
        other_files = []
        other_extensions = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', 
                           '.woff', '.woff2', '.ttf', '.eot', '.otf',
                           '.mp4', '.webm', '.mp3', '.wav', '.ogg')
        
        # Find all <a> tags with downloadable files
        for link in self.soup.find_all('a', href=True):
            href = link.get('href')
            if href and any(href.lower().endswith(ext) for ext in other_extensions):
                absolute_url = urljoin(self.url, href)
                other_files.append(absolute_url)
        
        # Find font files in <link> tags
        for link in self.soup.find_all('link', href=True):
            href = link.get('href')
            if href and any(href.lower().endswith(ext) for ext in ('.woff', '.woff2', '.ttf', '.eot', '.otf')):
                absolute_url = urljoin(self.url, href)
                other_files.append(absolute_url)
        
        # Find video sources
        for video in self.soup.find_all(['video', 'source'], src=True):
            src = video.get('src')
            if src:
                absolute_url = urljoin(self.url, src)
                other_files.append(absolute_url)
        
        # Find audio sources
        for audio in self.soup.find_all(['audio', 'source'], src=True):
            src = audio.get('src')
            if src:
                absolute_url = urljoin(self.url, src)
                other_files.append(absolute_url)
        
        return list(set(other_files))  # Remove duplicates
    
    def extract_colors(self) -> List[str]:
        """
        Extract colors from inline styles and style tags.
        
        Returns:
            List of color values (HEX, RGB, RGBA, color names)
        """
        if not self.soup:
            return []
        
        colors: Set[str] = set()
        
        # Regex patterns for different color formats
        hex_pattern = r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\b'
        rgb_pattern = r'rgb\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)'
        rgba_pattern = r'rgba\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)'
        hsl_pattern = r'hsl\s*\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*\)'
        
        # Extract from inline styles
        for element in self.soup.find_all(style=True):
            style = element.get('style', '')
            
            # Find all color patterns
            colors.update(re.findall(hex_pattern, style))
            colors.update(re.findall(rgb_pattern, style, re.IGNORECASE))
            colors.update(re.findall(rgba_pattern, style, re.IGNORECASE))
            colors.update(re.findall(hsl_pattern, style, re.IGNORECASE))
        
        # Extract from <style> tags
        for style in self.soup.find_all('style'):
            style_content = style.string or ''
            
            # Find all color patterns
            hex_colors = re.findall(hex_pattern, style_content)
            colors.update(['#' + c for c in hex_colors])
            colors.update(re.findall(rgb_pattern, style_content, re.IGNORECASE))
            colors.update(re.findall(rgba_pattern, style_content, re.IGNORECASE))
            colors.update(re.findall(hsl_pattern, style_content, re.IGNORECASE))
        
        # Clean up hex colors (remove duplicate # if present)
        cleaned_colors = []
        for color in colors:
            if color.startswith('#'):
                cleaned_colors.append(color)
            elif re.match(r'^[A-Fa-f0-9]{3,6}$', color):
                cleaned_colors.append('#' + color)
            else:
                cleaned_colors.append(color)
        
        return sorted(list(set(cleaned_colors)))
    
    def extract_fonts(self) -> List[str]:
        """
        Extract font families used in the website.
        
        Returns:
            List of font family names
        """
        if not self.soup:
            return []
        
        fonts: Set[str] = set()
        
        # Extract from inline styles
        for element in self.soup.find_all(style=True):
            style = element.get('style', '')
            font_families = re.findall(r'font-family\s*:\s*([^;]+)', style, re.IGNORECASE)
            for family in font_families:
                # Split by comma and clean up
                for font in family.split(','):
                    cleaned_font = font.strip().strip('"\'')
                    if cleaned_font:
                        fonts.add(cleaned_font)
        
        # Extract from <style> tags
        for style in self.soup.find_all('style'):
            style_content = style.string or ''
            font_families = re.findall(r'font-family\s*:\s*([^;}]+)', style_content, re.IGNORECASE)
            for family in font_families:
                # Split by comma and clean up
                for font in family.split(','):
                    cleaned_font = font.strip().strip('"\'')
                    if cleaned_font:
                        fonts.add(cleaned_font)
        
        # Extract from @font-face declarations
        for style in self.soup.find_all('style'):
            style_content = style.string or ''
            font_face_names = re.findall(r'@font-face\s*\{[^}]*font-family\s*:\s*["\']?([^"\';}]+)', 
                                         style_content, re.IGNORECASE | re.DOTALL)
            for font in font_face_names:
                cleaned_font = font.strip()
                if cleaned_font:
                    fonts.add(cleaned_font)
        
        return sorted(list(fonts))
    
    def build_file_structure(self, file_urls: List[str]) -> Dict[str, Any]:
        """
        Build a hierarchical file structure tree from URLs.
        
        Args:
            file_urls: List of file URLs
            
        Returns:
            Dictionary representing the file tree structure
        """
        structure = {}
        
        for url in file_urls:
            try:
                parsed = urlparse(url)
                path = parsed.path.strip('/')
                
                if not path:
                    continue
                
                parts = path.split('/')
                current = structure
                
                # Build nested dictionary structure
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:
                        # It's a file
                        current[part] = url
                    else:
                        # It's a directory
                        if part not in current:
                            current[part] = {}
                        if isinstance(current[part], dict):
                            current = current[part]
            except Exception:
                continue
        
        return structure