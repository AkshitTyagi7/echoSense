import json
from fastapi import Request, FastAPI

from fastapi.middleware.cors import CORSMiddleware
import detector
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/speaking")
async def read_root(request: Request):
        payload = await request.json()

        res = detector.guess(json.stringify(payload))
        print('This is result')
        print(res)
        return {
            'result': res
        }
