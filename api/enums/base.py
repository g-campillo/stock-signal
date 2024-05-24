from enum import Enum

class BaseEnum(Enum):
    
    def to_str(self) -> str:
        return self.name.lower()
    
    @classmethod
    def from_str(cls, value: str, default: str = None):
        try:
            return cls[value.upper()]
        except KeyError:
            if default is not None and isinstance(default, cls):
                return default
            raise