"""
JSON Loader: Utilities for loading and saving JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any


def load_json(path: str) -> Dict[str, Any]:
    """
    Load a JSON file.
    
    Args:
        path: Path to JSON file
    
    Returns:
        Parsed JSON as dictionary
    
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is invalid JSON
    """
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path: str, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        path: Path to JSON file
        data: Data to save
        indent: JSON indentation (default 2)
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)
