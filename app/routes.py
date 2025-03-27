from fastapi import APIRouter, HTTPException
from .models import PixPayment
from .gateways.pix_factory import get_pix_gateway

router = APIRouter()

@router.post("/pagar")
def pay_pix(payload: PixPayment, bank: str = "inter"):
    """
    Endpoint para realizar um pagamento via Pix.
    """
    try:
        gateway = get_pix_gateway(bank)
        result = gateway.process_payment(
            key=payload.key,
            amount=payload.amount,
            description=payload.description
        )
        return {
            "status": "sucesso",
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
