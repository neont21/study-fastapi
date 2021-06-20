Dependencies
===

```bash
$ pip3 install fastapi uvicorn
```

Extra Dependencies
---

To receive uploaded files,

```bash
$ pip3 install python-multipart
```

To use dependencies with yield,

```bah
$ pip3 install async-exit-stack async-generator
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