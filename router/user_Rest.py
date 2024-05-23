import os
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends,HTTPException
from model.user import UserBase
from security.security import validate_token
from service.services import generate_token
from service.user_DAO import all_users, check_customer, create_user, info_customer, existing_customer

load_dotenv()
secret_url_api = os.environ.get('SECURITY_URL_API')

router = APIRouter()

@router.get("/get-all-user", tags=["Users"])
async def get_all_users():
    users = all_users()
    return users

@router.get("/get-customer",dependencies=[Depends(validate_token)],tags=["Users"])
async def get_infor_customer(id:str = Depends(validate_token)):
    customer = info_customer(str(id))
    if customer:
        return customer
    raise HTTPException(status_code=404, detail=f"Customer {id} not found")

@router.post("/create-customer", tags=["Users"])
async def post_create_user(body:UserBase = Body(...)):
    body = body.dict()
    customer = existing_customer(body['username'])
    if customer:
        raise HTTPException(status_code=400, detail='Tài khoản đã tồn tại')
    create_user(body['fullname'],body['username'], body['password'],body['contact'],body['address'])
    return {'message': 'Tạo tài khoản thành công'}

@router.post("/login", tags=["Users"])
async def post_check_customer(body:UserBase = Body(...)):
    body = body.dict()
    customer = check_customer(body['username'], body['password'])
    if customer:
        token = generate_token(customer.id)
        return {'token': token}
    # Nếu thông tin đăng nhập không hợp lệ, trả về lỗi 401 Unauthorized
    raise HTTPException(status_code=401, detail='Đăng nhập không thành công')
    
@router.put("/update-user/{id}", tags=["Users"])
async def update_user():
    return
    
@router.delete("/delete-user/{id}", tags=["Users"])
async def delete_user():
    return

