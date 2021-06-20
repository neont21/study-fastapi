Dependencies
===

```bash
$ pip3 install fastapi uvicorn
```

Skeletone template
===

`main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'It\' work!'}
```

Execute command
===

```bash
$ uvicorn main:app --reload
```