import json
import os
from datetime import datetime
import uuid

class Persistable:
    """Base class for persistent objects with shared attributes."""
    objects = []

    @classmethod
    def load_all(cls):
        """Load all objects from JSON files in the current directory."""
        cls.objects = []
        for filename in os.listdir('.'):
            if filename.endswith('.json'):
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                   
                    if 'type' in data:
                        if data['type'] == 'Book':
                            obj = Book(**{k: v for k, v in data.items() if k != 'type'})
                        elif data['type'] == 'User':
                            obj = User(**{k: v for k, v in data.items() if k != 'type'})
                        else:
                            continue
                        cls.objects.append(obj)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def __init__(self, name, id=None, **kwargs):
        """Initialize object with name, id, and timestamps."""
        self.name = name
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id
        filename = self.name + '.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            self.__dict__.update(data)
            self.updated_at = datetime.now().isoformat()
        else:
            self.created_at = datetime.now().isoformat()
            self.updated_at = self.created_at
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.__class__.objects.append(self)