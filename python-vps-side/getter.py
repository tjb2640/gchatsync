from fastapi import FastAPI, Request, HTTPException, status
from os import remove
from os.path import exists
from bot import savedir
import time
import uvicorn

PORT = 8080
api_keys = { # auth token -> server name
    'snakeoil_east': 'east',
    'snakeoil_west': 'west'
}

app = FastAPI()

def read_and_clear_server_messages(server_name):
    fname = '%s/%s' % (savedir, server_name)
    msgs_json = '{}'
    if exists(fname):
        with open(fname, 'r') as f:
            msgs_json = f.read()
            f.close()
        remove(fname)
    if not (msgs_json == '{}'):
        print('[GET/%d] %s' % (int(time.time()), server_name))
    return msgs_json

@app.get('/egress')
async def post_egress(req: Request, token: str = ''):
    if (not token) or (token not in api_keys.keys()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    return read_and_clear_server_messages(api_keys[token])

if __name__ == "__main__":
    uvicorn.run(app, port=PORT)