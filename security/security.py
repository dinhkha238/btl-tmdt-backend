from datetime import datetime
import os
from dotenv import load_dotenv
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError

load_dotenv()
secret_algorithm = os.environ.get('SECURITY_ALGORITHM')
secret_algorithm_pass = os.environ.get('SECURITY_ALGORITHM_PASS')

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, secret_algorithm_pass, algorithms=[secret_algorithm])
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('_id')
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )