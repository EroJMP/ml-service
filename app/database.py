import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from app.config import DB_DIR

class JsonDatabase:
    """Simple JSON file-based database."""
    
    def __init__(self, collection_name: str):
        """Initialize the database with a collection name."""
        self.collection_name = collection_name
        self.db_file = DB_DIR / f"{collection_name}.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from the JSON file."""
        if not self.db_file.exists():
            return {}
        
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def _save_data(self) -> None:
        """Save data to the JSON file."""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all items in the collection."""
        return self.data
    
    def get(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get an item by ID."""
        return self.data.get(item_id)
    
    def create(self, item_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new item."""
        self.data[item_id] = item_data
        self._save_data()
        return item_data
    
    def update(self, item_id: str, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing item."""
        if item_id not in self.data:
            return None
        
        self.data[item_id] = item_data
        self._save_data()
        return item_data
    
    def delete(self, item_id: str) -> bool:
        """Delete an item."""
        if item_id not in self.data:
            return False
        
        del self.data[item_id]
        self._save_data()
        return True

# Create signature sets database
signature_sets_db = JsonDatabase("signature_sets") 