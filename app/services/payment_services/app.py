from fastapi import FastAPI

app = FastAPI(title='Payments Service')


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/version')
def version():
    return {"version": "0.1.0"}

