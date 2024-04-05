from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile, status, Response
import models

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "World"}


@app.post(
    "/statements/upload/{type}",
    status_code=status.HTTP_201_CREATED,
    response_model=models.Response
)
def statement_upload(file: UploadFile, type: str, response: Response) -> models.Response:
    if type.lower() not in models.STATEMENT_TYPES:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return models.Response(message="type is invalid", data=[])
    # return {"filename": file.filename, "type": type}
    return models.Response(message="success", data={
        "filename": file.filename,
        "type": type
    })


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
