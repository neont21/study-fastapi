import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import items, users, notify

tags_metadata = [
    {
        'name': 'users',
        'description': 'Operations with users. The **login** logic is also here.',
    },
    {
        'name': 'items',
        'description': 'Manage itesm. So _fancy_ they have their own docs.',
        'externalDocs': {
            'description': 'Item external docs',
            'url': 'https://fastapi.tiangolo.com',
        },
    },
]

app = FastAPI(
    title='My Super Project',
    description='This is a very fancy project, with auto docs for the API and everything',
    version='2.5.0',
    openapi_tags=tags_metadata,
    openapi_url='/api/v1/openapi.json',
    docs_url='/document',
)

app.include_router(items.router)
app.include_router(users.router)
app.include_router(notify.router)

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/')
async def root():
    return {'msg': 'Hello World'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)