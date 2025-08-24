import re
# Utility functions to sanitize user input
# Helps prevent malicious scripts (XSS) or dirty data

def sanitize_text(text: str) -> str:
    """
    Sanitize text by:
    - Stripping leading/trailing whitespace
    - Removing HTML/JS tags
    - Allowing only safe characters (alphanumeric, spaces, commas, periods, dashes)
    """
    if not text:
        return ""

    # Remove HTML tags
    clean = re.sub(r'<.*?>', '', text)

    # Allow only safe characters (letters, numbers, spaces, commas, periods, dashes)
    clean = re.sub(r'[^\w\s,.-]', '', clean)

    return clean.strip()
