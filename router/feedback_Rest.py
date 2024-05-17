from fastapi import APIRouter, Body, Depends

from model.feedback import FeedbackBase
from security.security import validate_token
from service.feedback_DAO import add_feedback, feedback_by_id_product



router = APIRouter()

@router.get("/feedback-by-id-product/{product_id}", tags=["Feedback"])
async def get_feedback_by_id_product(product_id: int):
    feedback = feedback_by_id_product(product_id)
    return feedback

@router.post("/add-feedback", tags=["Feedback"], dependencies=[Depends(validate_token)])
async def post_add_feedback(feedback: FeedbackBase = Body(...),id:str = Depends(validate_token)):
    add_feedback(feedback,id)
    return feedback