'''
The submodule dedicated to handling the administrator tasks
'''
from fastapi import APIRouter, Depends
from ..dependencies import get_query_token

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_query_token)],
    responses={418: {'description': 'I\'m a teapot'}})

@router.post('')
async def update_admin():
    return {'message': 'Admin getting schwifty'}
