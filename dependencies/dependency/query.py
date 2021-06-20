from typing import Optional
from fastapi import Cookie, Depends
from fastapi.param_functions import Query

def query_extractor(
    q: Optional[str] = Query(
        None,
        title='Query',
        description='Query to execute.',
    ),
):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Cookie(
        None,
        title='Last Query',
        description='Query excuted last.'
    ),
):
    if not q:
        return last_query
    return q
