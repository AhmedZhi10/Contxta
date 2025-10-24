# in: app/core/security.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from app.core.config import settings

# This scheme tells FastAPI how to extract the token from the
# 'Authorization: Bearer <TOKEN>' header.
# The tokenUrl is just a placeholder as this service only verifies tokens.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenPayload(BaseModel):
    """
    Defines the expected shape of the data inside the JWT token.
    We expect at least a 'sub' (subject) claim containing the user ID.
    """
    sub: str # Standard JWT claim for the subject (user identifier)

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Dependency that verifies the JWT token and returns its payload (containing user_id).
    This function will protect our endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using the secret key and algorithm from settings
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        # Extract the user ID from the 'sub' claim
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception # Token is missing the user ID
        
        # Validate the payload structure (ensures 'sub' is a string)
        token_data = TokenPayload(sub=user_id)
        
    except (JWTError, ValidationError):
        # If decoding fails or payload is invalid, raise the exception
        raise credentials_exception
        
    return token_data