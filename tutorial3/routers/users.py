'''
The submodule dedicated to handling just users
'''
from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['users'])

@router.get('')
async def get_users():
    return [
        {'name': 'Harry'},
        {'name': 'Ron'},
    ]
