from typing import Optional
from fastapi import Depends, FastAPI, Query, status
from model import CommonQueryParams
from dependency import query_or_cookie_extractor, verify_token, verify_key

app = FastAPI(
    dependencies=[Depends(verify_token), Depends(verify_key)],
)

fake_items_db = [
    {"item_name": "Foo"}, 
    {"item_name": "Bar"}, 
    {"item_name": "Baz"}
]

async def common_parameters(
    q: Optional[str] = Query(
        None,
        title='Query',
    ),
    skip: int = Query(
        0,
        title='Skip index',
    ),
    limit: int = Query(
        100,
        title='Limit index',
    ),
):
    return {
        'q': q,
        'skip': skip,
        'limit': limit,
    }

@app.get('/items', tags=['item'])
async def read_item(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({'q': commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({'items': items})
    return commons

@app.post('/users', tags=['user'], 
    status_code=status.HTTP_201_CREATED)
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

@app.get('/query', tags=['query'])
async def read_query(
    query_or_default: str = Depends(
        query_or_cookie_extractor,
    ),
):
    return {'q_or_cookie': query_or_default}

@app.get('/items/pro', tags=['item'],
    dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_item_pro():
    return [
        {'item': 'Foo'},
        {'item': 'Bar'},
    ]