from typing import Union, Annotated, Optional
from fastapi import FastAPI, File, UploadFile, status, Response, Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
import models
import util
import Statement
import pathlib
from fastapi.responses import FileResponse
from jose import JWTError, jwt


app = FastAPI()

get_bearer_token = HTTPBearer(auto_error=False)


def get_token(auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = auth.credentials
        if token is None:
            raise credentials_exception
        payload = jwt.decode(token, util.SECRET_KEY,
                             algorithms=[util.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
        if token_data.username is None or token_data.username == "" or token_data.username != util.USERNAME:
            raise credentials_exception
    except (JWTError) as err:
        print(err)
        raise credentials_exception


@app.get("/")
def read_root():
    return {"message": "World"}


@app.post(
    "/statements/upload/{type}",
    status_code=status.HTTP_201_CREATED,
    response_model=models.Response,
)
def statement_upload(token: Annotated[str, Depends(get_token)], file: UploadFile, type: str, response: Response) -> models.Response:
    try:
        if type.lower() not in models.STATEMENT_TYPES:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return models.Response(message="type is invalid", data=[])

        filename = util.rand_string(10)
        path = pathlib.Path().absolute() / f"./uploads/{filename}.pdf"
        util.save_upload_file(file, path)

        outPath = Statement.Statement(
            type).getStatement(pdfPath=path, type=type, filename=filename)

        if outPath[0] == False:
            response.status_code = outPath[1]
            return models.Response(message=outPath[2], data=[])

        return FileResponse(outPath, content_disposition_type="attachment", media_type="text/csv", filename=f"{filename}.csv")
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return models.Response(message=f"{e}", data=[])
    # return models.Response(message="success", data={
    #     "filename": file.filename,
    #     "type": type,
    # })


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
