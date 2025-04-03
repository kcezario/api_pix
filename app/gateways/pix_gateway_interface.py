from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PixGateway(ABC):
    
    @abstractmethod
    def get_config(self) -> dict:
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        pass

    @abstractmethod
    def process_payment(self, key: str, amount: float, description: str) -> dict:
        pass
        
    @abstractmethod
    def get_payment_status(self, transaction_id: str) -> dict:
        pass
