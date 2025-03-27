from fastapi import APIRouter, HTTPException
from app.models import PixPayment
from app.inter_api import process_pix_payment

router = APIRouter()

@router.post("/pagar")
def pay_pix(payload: PixPayment):
    """
    Endpoint para realizar um pagamento via Pix.
    """
    try:
        result = process_pix_payment(
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