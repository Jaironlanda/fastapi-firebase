
import os
import firebase_admin
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.encoders import jsonable_encoder

from firebase_admin import credentials, auth, exceptions

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List
from dotenv import load_dotenv

load_dotenv()
# from .db.models import Team, User
# from .db.config import get_session
# from .db.utils import create_user, create_team, get_user, get_all_user, get_team_with_user, get_all_team, delete_user_with_id, update_user_by_id
# from .db.schemas import TeamBase, User, UserBase, TeamWithUser, Team, UserCreate

from .db.schemas import SignupBase

# Please don't share your firebase admin cert!
# Use environment instead
firebase_cert = {
  "type": os.getenv('FIREBASE_TYPE'),
  "project_id": os.getenv('FIREBASE_PROJECT_ID'),
  "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
  "private_key": os.getenv('FIREBASE_PRIVATE_KEY'),
  "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
  "client_id": os.getenv('FIREBASE_CLIENT_ID'),
  "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
  "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
  "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_CERT_URL'),
  "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
}

init_cred = credentials.Certificate(firebase_cert)
firebase_admin.initialize_app(init_cred)

router = APIRouter(prefix="/api/v1")

# Referance: https://stackoverflow.com/questions/64190757/fastapi-security-with-firebase-token
async def verify_token(res: Response, cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))):
  try:
    decoded_token = auth.verify_id_token(cred.credentials ,check_revoked=True)
  except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid authentication credentials. {e}",
        headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
    )
  res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'

  return decoded_token

# Example create new user from firebase admin
@router.post('/signup')
async def signup(signup: SignupBase):
  print(type(signup.email))
  try:
    user = auth.create_user(  
      email=signup.email,
      password=signup.password
    )

    return jsonable_encoder(user)

  except auth.EmailAlreadyExistsError:
    return {'message': 'Email already exist!'}

# Get user profile base on access token.
@router.get('/profile')
async def profile(user: str = Depends(verify_token)):
  return auth.get_user(user['uid'])

# Edit user, please refer firebase doc for furter info
@router.put('/profile/edit')
async def profile_edit(user: str = Depends(verify_token)):
  try:
    print(user)
    update_user = auth.update_user(
      uid=user['uid'],
      display_name='Jairon Landa'
    )
    return update_user
  except exceptions.FirebaseError as e:
    return e

# No need authentication Bearer, this is admin mode
# For more info, please visit official Doc: https://firebase.google.com/docs/auth/admin/manage-users
@router.get('/user')
async def get_user_email(email: str):
    return auth.get_user_by_email(email)

@router.delete('/delete')
async def delete_user(uid: str):
    return auth.delete_user(uid)

@router.get('/user/{uid}')
async def get_user(uid: str):
    return auth.get_user(uid)

@router.get('/firebase/alluser')
async def firebase_auth_alluser():
    page = auth.list_users()

    return {'user': page.users}

    