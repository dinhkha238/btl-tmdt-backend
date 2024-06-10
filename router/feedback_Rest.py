from fastapi import APIRouter, Body, Depends

from dbconnect import SessionLocal
from model.feedback import FeedbackBase
from security.security import validate_token
from service.feedback_DAO import add_feedback, feedback_by_id_product



router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/feedback-by-id-product/{product_id}", tags=["Feedback"])
async def get_feedback_by_id_product(product_id: int, db = Depends(get_db)):
    feedback = feedback_by_id_product(product_id, db)
    return feedback

@router.post("/add-feedback", tags=["Feedback"], dependencies=[Depends(validate_token)])
async def post_add_feedback(feedback: FeedbackBase = Body(...),id:str = Depends(validate_token),db = Depends(get_db)):
    add_feedback(feedback,id,db)
    return feedback