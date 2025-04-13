#!/usr/bin/python3
"""Defines a BaseModel class with serialization and deserialization logic."""

import uuid
from datetime import datetime
import models

class BaseModel:
    """Base class for all models with common attributes and methods."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        If kwargs is provided, use it to set attributes.
        Otherwise, generate default values.
        """
        if kwargs and len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                if key != "__class__": # Skip key with __class__
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the BaseModel."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the `updated_at` attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing all keys/values of the instance."""
        dict_rep =self.__dict__.copy()
        dict_rep["__class__"] = self.__class__.__name__
        dict_rep["created_at"] = self.created_at.isoformat()
        dict_rep["updated_at"] = self.updated_at.isoformat()
        return dict_rep
