from abc import ABC, abstractmethod


class IFileHandler(ABC):
    
    @abstractmethod
    def save(content: str, output_path: str):
        pass