"""
Utility helper functions
"""
import logging
import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
import re


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup application logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('confluence_enhancer.log')
        ]
    )
    return logging.getLogger(__name__)


def generate_hash(content: str) -> str:
    """Generate SHA256 hash for content"""
    return hashlib.sha256(content.encode()).hexdigest()


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
    return text.strip()


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)


def validate_confluence_url(url: str) -> bool:
    """Validate if URL is a valid Confluence page URL"""
    confluence_patterns = [
        r'.*confluence.*pages.*',
        r'.*wiki.*display.*',
        r'.*spaces.*',
    ]
    return any(re.search(pattern, url, re.IGNORECASE) for pattern in confluence_patterns)


def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks for AI processing"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start + chunk_size // 2:
                end = sentence_end + 1
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON with fallback"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format timestamp for display"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def extract_table_data(html_table: str) -> Dict[str, Any]:
    """Extract structured data from HTML table"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_table, 'html.parser')
    table = soup.find('table')
    
    if not table:
        return {'headers': [], 'rows': []}
    
    headers = []
    rows = []
    
    # Extract headers
    header_row = table.find('thead')
    if header_row:
        headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
    else:
        # Use first row as headers if no thead
        first_row = table.find('tr')
        if first_row:
            headers = [th.get_text().strip() for th in first_row.find_all(['th', 'td'])]
    
    # Extract data rows
    tbody = table.find('tbody') or table
    for row in tbody.find_all('tr'):
        if row == table.find('tr') and not table.find('thead'):
            continue  # Skip header row if we used it as headers
        
        cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
        if cells:
            rows.append(cells)
    
    return {'headers': headers, 'rows': rows}


def detect_data_types(data: List[List[str]]) -> List[str]:
    """Detect data types for table columns"""
    if not data:
        return []
    
    num_cols = len(data[0]) if data else 0
    types = ['text'] * num_cols
    
    for col_idx in range(num_cols):
        column_values = [row[col_idx] for row in data if col_idx < len(row)]
        
        # Check if numeric
        numeric_count = 0
        date_count = 0
        
        for value in column_values:
            if not value:
                continue
                
            # Check for numeric
            try:
                float(value.replace(',', '').replace('$', '').replace('%', ''))
                numeric_count += 1
            except ValueError:
                pass
            
            # Check for date
            if re.match(r'\d{4}-\d{2}-\d{2}', value) or re.match(r'\d{1,2}/\d{1,2}/\d{4}', value):
                date_count += 1
        
        total_values = len([v for v in column_values if v])
        if total_values == 0:
            continue
            
        if numeric_count / total_values > 0.8:
            types[col_idx] = 'numeric'
        elif date_count / total_values > 0.8:
            types[col_idx] = 'date'
    
    return types


logger = setup_logging()
