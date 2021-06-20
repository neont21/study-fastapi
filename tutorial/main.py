from starlette.responses import JSONResponse, PlainTextResponse
from model import Image, Item, ModelName, Offer, UserIn, UserOut, UnicornException
from feature import fake_save_user
from typing import List, Dict, Optional
from fastapi import FastAPI, Path, Query, Body, Header, Form, File, UploadFile, status, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from uuid import UUID

app = FastAPI()

items = {
    "foo": {
        "name": "Foo", 
        "price": 50.2
    },
    "bar": {
        "name": "Bar", 
        "description": "The Bar fighters", 
        "price": 62, 
        "tax": 20.2
    },
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get(
    '/',
    summary='Main page',
)
async def root():
    '''
    The main page of the system.
    '''
    content = '''
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    '''
    return HTMLResponse(content=content)

@app.post(
    '/items', 
    response_model=Item,
    response_model_exclude_unset=True,
    response_model_exclude_defaults=True,
    status_code=status.HTTP_201_CREATED,
    tags=['items'],
    summary='Create an item',
    response_description='The created item',
)
async def create_item(
    item: Item = Body(
        ...,
        title='The item data',
        description='the data of the item',
	    example={
            'name': 'Foo',
            'description': 'A very nice Item',
            'price': 35.4,
            'tax': 3.2,
	    },
    ),
):
    '''
    Create an item with all the information:

    - **name** : each item must have a name
    - **description** : a long description
    - **price** : required
    - **tax** : if the item doesn't have tax, you can omit this
    - **tags** : a set of unique tag strings for this item
    '''
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    items.update(item_dict)
    return item_dict

@app.post(
    '/items/{item_id}',
    status_code=status.HTTP_201_CREATED,
    tags=['items'],
)
async def create_item(
    item: Item = Body(
        ...,
        title='The item data',
        description='The data of the item',
	    example={
            'name': 'Foo',
            'description': 'A very nice Item',
            'price': 35.4,
            'tax': 3.2,
	    },
    ), 
    item_id: UUID = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
    q: Optional[str] = Query(
        None,
        title='Query String', 
        description='Query string for the items to search in the database that have a good match',
        example='query',
    )
):
    '''
    Create the item information by JSON.
    '''
    result = {'item_id': item_id, **item.dict()}
    if q:
        result.update({'q': q})
    return result

@app.get(
    '/items',
    tags=['items'],
)
async def read_item(
    user_agent: Optional[str] = Header(
        None,
        example='Mozilla/5.0',
    ),
    x_token: Optional[List[str]] = Header(
        None,
        example=['foo', 'bar'],
    ),
    q: Optional[List[str]] = Query(
        ['foo', 'bar'], 
        title='Query String', 
        description='Query string for the items to search in the database that have a good match',
        example=['foo', 'bar'],
    ),
):
    '''
    Get the item information.
    '''
    results = {
        'items': [
            {'item_id': 'Foo'}, 
            {'item_id': 'Bar'}
        ],
        'User-Agent': user_agent,
        'X-Token values': x_token,
    }
    if q:
        results.update({'q': q})
    return results

@app.get(
    '/items/{item_id}',
    tags=['items'],
)
async def read_item(
    item_id: UUID = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
    q: Optional[str] = Query(
        None,
        title='Query String', 
        description='Query string for the items to search in the database that have a good match',
        example='query',
    ), 
    short:bool = Query(
        False,
        title='Short Indicator',
        description='A value indicating whethere the item has a long description',
        example=False,
    ),
):
    '''
    Get the item information by ID.
    '''
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found',
            headers={
                'X-Error': 'There goes my errpr',
            },
        )
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})
    return item

@app.get(
    '/items/{item_id}/name',
    response_model=Item,
    response_model_include={'name', 'description'},
    tags=['items'],
)
async def read_item_name(
    item_id: str = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
):
    '''
    Read the name of the item
    '''
    return items[item_id]

@app.get(
    '/items/{item_id}/public',
    response_model=Item,
    response_model_exclude=['tax'],
    tags=['items'],
)
async def read_item_public_data(
    item_id: str = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
):
    '''
    Read the public data of the item
    '''
    return items[item_id]

@app.put(
    '/items/{item_id}',
    response_model=Item,
    tags=['items'],
    summary='Update the item',
)
async def update_item(
    item_id: str = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
    item: Item = Body(
        ...,
        title='The item data',
        description='the data of the item',
	    example={
            'name': 'Foo',
            'description': 'A very nice Item',
            'price': 35.4,
            'tax': 3.2,
	    },
    ),
):
    '''
    Identify the item with `item_id`    

    Update the item with all information:

    - **name** : each item must have a name
    - **description** : a long description
    - **price** : required
    - **tax** : if the item doesn't have tax, you can omit this
    - **tags** : a set of unique tag strings for this item
    '''
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.patch(
    '/items/{item_id}',
    response_model=Item,
    tags=['items'],
    summary='Update the item partially',
)
async def update_item(
    item_id: str = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
    item: Item = Body(
        ...,
        title='The item data',
        description='the data of the item',
	    example={
            'name': 'Foo',
            'description': 'A very nice Item',
            'price': 35.4,
            'tax': 3.2,
	    },
    ),
):
    '''
    Identify the item with `item_id`    

    Update the item with some of the information:

    - **name** : each item must have a name
    - **description** : a long description
    - **price** : required
    - **tax** : if the item doesn't have tax, you can omit this
    - **tags** : a set of unique tag strings for this item
    '''
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

@app.post(
    '/users',
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=['users'],
    )
async def create_user(
    user_in: UserIn = Body(
        ...,
        example={
            'username': 'peeeeeter_j',
            'password': 'ku201711424',
            'email': 'peter.j@kakao.com',
            'full_name': 'Peter Johannes Jung',
        }
    ),
):
    '''
    Create the user account.
    '''
    user_saved = fake_save_user(user_in)
    return user_saved

@app.get(
    '/users/me',
    tags=['users'],
)
async def read_user_me():
    '''
    Get the user information of the current user.
    '''
    return {'user_id': 'the current user'}

@app.get(
    '/users/{user_id}',
    tags=['users'],
)
async def read_user(
    user_id: str = Path(
        ...,
        title='User ID',
        description='The ID of the user',
        example=78,
    ),
):
    '''
    Get the user information by ID.
    '''
    return {'user_id': user_id}

@app.get(
    '/users/{user_id}/items/{item_id}',
    tags=['items'],
)
async def read_user_item(
    user_id: str = Path(
        ...,
        title='User ID',
        description='The ID of the user',
        example=78,
    ),
    item_id: UUID = Path(
        ...,
        title='Item ID',
        description='The ID of the item',
        example='pt',
    ),
    q: Optional[str] = Query(
        None,
        title='Query String', 
        description='Query string for the items to search in the database that have a good match',
        example='query',
    ),
    short:bool = Query(
        False,
        title='Short Indicator',
        description='A value indicating whethere the item has a long description',
        example=False,
    ),
):
    '''
    Get the user information and the item information by ID.
    '''
    item = {'item_id': item_id, 'user_id': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'description': 'This is an amazing item that has a long description'})
    return item

@app.post(
    '/login',
    status_code=status.HTTP_201_CREATED,
    tags=['users'],
)
async def login(
    username: str = Form(
        ...,
    ),
    password: str = Form(
        ...,
    ),
):
    return {'username': username}

@app.post(
    '/files',
    status_code=status.HTTP_201_CREATED,
    tags=['files'],
)
async def create_file(
    file: bytes = File(
        ...,
    ),
    fileb: UploadFile = File(
        ...,
    ),
    token: str = Form(
        ...,
    ),
):
    return {
        'file_sizes': len(file),
        'token': token,
        'fileb_content_type': fileb.content_type,
    }

@app.post(
    '/uploadfiles',
    status_code=status.HTTP_201_CREATED,
    tags=['files'],
)
async def create_upload_file(
    files: List[UploadFile] = File(
        ...,
    ),
):
    return {'filename': [file.filename for file in files]}

@app.get(
    '/models/{model_name}',
    tags=['models'],
)
async def get_model(
    model_name: ModelName = Path(
        ...,
        title='Model Name',
        description='the name of the model',
        example=ModelName.alexnet,
    ),
):
    '''
    Get the model information by name.
    '''
    match model_name:
        case ModelName.alexnet:
            return {'model_name': model_name, 'message': 'Deep Learning FTW!'}
        case ModelName.lenet:
            return {'model_name': model_name, 'messaeg': 'LeCNN all the images'}
        case _:
            return {'model_name': model_name, 'message': 'Have some residuals'}

@app.post(
    '/offers',
    status_code=status.HTTP_201_CREATED,
    tags=['items'],
)
async def create_offer(
    offer: Offer = Body(
        ...,
        title='The Offer data',
        description='The data of the offer',
        example={
            'name': 'Foo',
            'description': 'The description of the offer',
            'price': 35.4,
            'items': [{
                'name': 'Foo',
                'description': 'The description of the item',
                'price': 35.4,
                'tax': 3.2,
            }],
        }
    ),
):
    '''
    Create new offer.
    '''
    return offer

@app.post(
    '/images/multiple',
    status_code=status.HTTP_201_CREATED,
    tags=['items'],
)
async def create_multiple_images(
    images: List[Image] = Body(
        ...,
	    title='The image list',
	    description='The list of the image data',
        example=[{
            'url': 'http://host.url/path/to/the/image/file',
            'name': 'Foo',
        }]
    ),
):
    '''
    Create the multiple image data.
    '''
    return images

@app.post(
    '/index-weights',
    status_code=status.HTTP_201_CREATED,
    tags=['items'],
)
async def create_index_weights(
    weights: Dict[int, float] = Body(
        ...,
	    title='The weights data',
	    descrption='Create the dictionary of (index, weight) of the data.',
        example={0: 3.14}
    ),
):
    '''
    Create the index weights.
    '''
    return weights

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(
    request: Request,
    exc: UnicornException,
):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={
            'message': f'Oops! {exc.name} did something. There goes a rainbow...',
        },
    )

@app.get(
    '/unicorns/{name}',
    tags=['unicorns'],
)
async def read_unicorm(
    name: str = Query(
        ...,
        example='yolo',
    ),
):
    if name == 'yolo':
        raise UnicornException(name=name)
    return {'unicorn_name': name}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: UnicornException,
):
    return PlainTextResponse(
        str(exc),
        status_code=status.HTTP_400_BAD_REQUEST
    )
