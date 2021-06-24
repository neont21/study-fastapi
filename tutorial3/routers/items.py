'''
The submodule dedicated to handling just items
'''
from typing import Optional
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix='/items',
    tags=['items'])

fake_secret_token = 'coneofsilence'

fake_db = {
    'foo': {
        'id': 'foo', 
        'title': 'Foo', 
        'description': 'There goes my hero'},
    'bar': {
        'id': 'bar',
        'title': 'Bar',
        'description': 'The bartenders'},
    }

class Item(BaseModel):
    id: str
    title: str
    description: Optional[str] = None

@router.get('')
async def get_items():
    return [
        {'name': 'wand'},
        {'name': 'flying broom'},
    ]

@router.get('/{item_id}', response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid X-Token header')
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found')
    return fake_db[item_id]

@router.post('', response_model=Item,
    status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid X-Token header')
    if item.id in fake_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Item already exists')
    return item
