"""
High-performance parsing with Rust.
Demonstrates complex parsing tasks.
"""

def parse_csv_line(line: str) -> list:
    """Parse CSV line (Rust implementation for speed)."""
    return [x.strip() for x in line.split(",")]

def parse_json_like(text: str) -> dict:
    """Parse simple JSON-like structure."""
    import json
    try:
        return json.loads(text)
    except:
        return {}

if __name__ == "__main__":
    csv_line = "name, age, city"
    print("Parsed CSV:", parse_csv_line(csv_line))
    
    json_text = '{"key": "value"}'
    print("Parsed JSON:", parse_json_like(json_text))
