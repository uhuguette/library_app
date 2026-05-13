import json
import os
from datetime import datetime
import uuid

class Persistable:
    """Base class for persistent objects with shared attributes."""
    objects = []