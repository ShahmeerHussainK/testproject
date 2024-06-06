from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Define your secret key and algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create a password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the plain password matches the hashed password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a password.

    Args:
        password (str): The plain password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): Data to encode in the token.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def signup(db: Session, user: UserCreate) -> User:
    """
    Registers a new user.

    Args:
        db (Session): Database session object.
        user (UserCreate): User registration details.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException: If the email is already registered.
        SQLAlchemyError: If there is an issue with the database transaction.
    """
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error occurred: {e}")
        raise HTTPException(status_code=400, detail="Email already registered")


def login(db: Session, user: UserLogin) -> Optional[str]:
    """
    Logs in a user and returns an access token if authentication succeeds.

    Args:
        db (Session): Database session object.
        user (UserCreate): User credentials.

    Returns:
        Optional[str]: Access token if authentication succeeds, else None.
    """
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        access_token = create_access_token(data={"sub": db_user.email})
        return access_token
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieves the current user based on the JWT token.

    Args:
        db (Session): Database session object.
        token (str): JWT token.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the credentials are invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
