from typing import List, Set, Optional
from pydantic import BaseModel, Field, HttpUrl

class Image(BaseModel):
    '''
    Class for the image information
    '''
    url: HttpUrl = Field(
        ...,
        example='http://host.url/path/to/the/image/file'
    )
    name: str = Field(
        ...,
        example='Foo',
    )

class Item(BaseModel):
    '''
    Class for the item information
    '''
    name: str = Field(
        ...,
        example='Foo',
    )
    description: Optional[str] = Field(
        None,
        title='The description of the item',
        example='A very nice Item',
        max_length=300,
    )
    price: float = Field(
        ...,
        description='The price must be greater than zero',
        example=35.4,
        gt=0,
    )
    tax: Optional[float] = Field(
        None,
        example=3.2
    )
    tags: Set[str] = set()
    image: Optional[List[Image]] = Field(
        None,
        title='Image List',
        example=[{
            'url': 'http://host.url/path/to/the/image/file',
            'name': 'Foo',
        }],
    )

class Offer(BaseModel):
    '''
    Class for the offer data
    '''
    name: str = Field(
        ...,
        example='Foo',
    )
    description: Optional[str] = Field(
        None,
        example='The description of the offer',
    )
    price: float = Field(
        ...,
        example=35.4,
    )
    items: List[Item] = Field(
        ...,
        title='Item List',
        example=[{
            'name': 'Foo',
            'description': 'A very nice Item',
            'price': 35.4,
            'tax': 3.2,
        }],
    )