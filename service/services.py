from datetime import datetime, timedelta
import os
from typing import Union, Any
from dotenv import load_dotenv
import jwt

load_dotenv()
secret_algorithm = os.environ.get('SECURITY_ALGORITHM')
secret_algorithm_pass = os.environ.get('SECURITY_ALGORITHM_PASS')


def generate_token(id: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60*60000*24   
    )
    to_encode = {   
        "exp": expire, "_id": id
    }
    encoded_jwt = jwt.encode(to_encode, secret_algorithm_pass, algorithm=secret_algorithm)
    return encoded_jwt
