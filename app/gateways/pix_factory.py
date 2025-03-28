from .inter_pix_gateway import InterPixGateway
from .mock_pix_gateway import MockPixGateway
from .pix_gateway_interface import PixGateway

def get_pix_gateway(bank: str = "inter", account_number: str | None = None) -> PixGateway:
    """
    Retorna a implementação do PixGateway de acordo com o banco escolhido.
    
    Parâmetros:
    - bank: Nome do banco
    - account_number: Número da conta corrente (opcional)
    """
    bank = bank.lower()

    if bank == "inter":
        return InterPixGateway(account_number=account_number)
    elif bank == "mock":
        return MockPixGateway()
    else:
        raise ValueError(f"Banco '{bank}' não suportado. Use 'inter' ou 'mock'.")
