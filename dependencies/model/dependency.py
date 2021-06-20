from typing import Optional
from fastapi import Query

class CommonQueryParams:
    def __init__(
        self,
        q: Optional[str] = Query(
            None,
            title='Query',
            description='Query to execute.',
        ),
        skip: int = Query(
            0,
            title='Skip index',
            description='Determine how many items to skip.',
        ),
        limit: int = Query(
            100,
            title='Limit index',
            description='Determine the maximum count of the item.',
        ),
    ):
        self.q = q
        self.skip = skip
        self.limit = limit
