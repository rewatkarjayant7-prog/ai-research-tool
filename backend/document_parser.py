import pdfplumber
import io

def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using pdfplumber."""
    text_content = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        return "\n".join(text_content)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

def parse_txt(file_bytes: bytes) -> str:
    """Extract text from a TXT file."""
    try:
        return file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Fallback to other common encodings
        try:
            return file_bytes.decode('latin-1')
        except Exception as e:
            raise ValueError(f"Failed to decode TXT file: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse TXT file: {str(e)}")

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text based on file extension."""
    filename_lower = filename.lower()
    if filename_lower.endswith('.pdf'):
        return parse_pdf(file_bytes)
    elif filename_lower.endswith('.txt'):
        return parse_txt(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT document.")
