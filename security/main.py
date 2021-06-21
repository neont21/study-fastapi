from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from model import User, Token
from feature import fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, authenticate_user, create_access_token

app = FastAPI()

@app.post('/token', tags=['verify'], response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    '''
    Get access token if the user exists and is active.
    '''
    user = authenticate_user(fake_users_db,
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }

@app.get('/users/me', tags=['user'], response_model=User,
    summary='Get current user data')
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@app.get('/users/me/items', tags=['item'],
    summary='Get the items of current user')
async def read_own_items(
    current_user: User = Depends(get_current_active_user)
):
    return [{'item_id': 'Foo', 'owner': current_user.username}]
