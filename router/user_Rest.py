import os
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends,HTTPException
from dbconnect import SessionLocal
from model.user import UserBase
from security.security import validate_token
from service.services import generate_token
from service.user_DAO import all_users, check_customer, create_user, delete_user, info_customer, existing_customer, update_user

load_dotenv()
secret_url_api = os.environ.get('SECURITY_URL_API')

router = APIRouter()

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-all-user", tags=["Users"])
async def get_all_users(db = Depends(get_db)):
    users = all_users(db)
    return users

@router.get("/get-customer",dependencies=[Depends(validate_token)],tags=["Users"])
async def get_infor_customer(id:str = Depends(validate_token),db = Depends(get_db)):
    customer = info_customer(str(id),db)
    if customer:
        return customer
    raise HTTPException(status_code=404, detail=f"Customer {id} not found")

@router.post("/create-customer", tags=["Users"])
async def post_create_user(body:UserBase = Body(...),db = Depends(get_db)):
    body = body.dict()
    customer = existing_customer(body['username'],db)
    if customer:
        raise HTTPException(status_code=400, detail='Tài khoản đã tồn tại')
    create_user(body['fullname'],body['username'], body['password'],body['contact'],body['address'],body['gender'],body['birth'],db)
    return {'message': 'Tạo tài khoản thành công'}

@router.post("/login", tags=["Users"])
async def post_check_customer(body:UserBase = Body(...),db = Depends(get_db)):
    body = body.dict()
    customer = check_customer(body['username'], body['password'],db)
    if customer:
        token = generate_token(customer.id)
        return {'token': token}
    # Nếu thông tin đăng nhập không hợp lệ, trả về lỗi 401 Unauthorized
    raise HTTPException(status_code=401, detail='Đăng nhập không thành công')
    
@router.put("/update-user/{id}",dependencies=[Depends(validate_token)], tags=["Users"])
async def put_update_user(id:str,body:UserBase = Body(...),db = Depends(get_db)):
    body = body.dict()
    update_user(id,body,db)
    return {'message': 'Cập nhật thông tin thành công'}
    
@router.delete("/delete-user/{id}", tags=["Users"])
async def delete_delete_user(id:str, db = Depends(get_db)):
    delete_user(id,db)
    return {'message': 'Xóa tài khoản thành công'}

