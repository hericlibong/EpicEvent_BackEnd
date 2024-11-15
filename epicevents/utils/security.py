from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta

# Charger la clé secrète depuis les variables d'environnement
SECRET_KEY = os.getenv('SECRET_KEY', 'defaut_secret_key here')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30   # Durée de validité du token en minutes

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expiré")
        return None
    except jwt.InvalidTokenError:
        print("Token invalide")
        return None


# Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def hash_password(password: str) -> str:
    """
    Hash le mot de passe en utilisant bcrypt
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe en clair correspond au mot de passe hashé
    """
    return pwd_context.verify(plain_password, hashed_password)

