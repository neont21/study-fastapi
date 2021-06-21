Dependencies
===

```bash
$ pip3 install fastapi uvicorn
```

Extra Dependencies
---

To receive uploaded files,    
or    
To use OAuth2,    
(Cuz they use "form data" for sending the data)

```bash
$ pip3 install python-multipart
```

To use dependencies with yield,

```bash
$ pip3 install async-exit-stack async-generator
```

To generate and verify the JWT tokens,

```bash
$ pip3 install python-jose[cryptography]
```

To handle password hashes,

```bash
$ pip3 install passlib[bcrypt]
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
