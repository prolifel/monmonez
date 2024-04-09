from functools import lru_cache
from jose import JWTError, jwt
from fastapi.responses import FileResponse
import pathlib
import Statement
import util
import models
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import FastAPI, UploadFile, status, Response, Depends, HTTPException
from typing import Annotated
from config import Settings


@lru_cache
def get_settings():
    return Settings()


config = {}


def lifespan(app: FastAPI):
    try:
        print("starting lifespan")
        config["env"] = get_settings()
        if config["env"].ACCESS_TOKEN_EXPIRE_MINUTES is None or config["env"].ACCESS_TOKEN_EXPIRE_MINUTES == 0 or config["env"].SECRET_KEY is None or config["env"].SECRET_KEY == "" or config["env"].ALGORITHM is None or config["env"].ALGORITHM == "" or config["env"].APP_USER is None or config["env"].APP_USER == "":
            raise Exception("missing config")
    except Exception as e:
        print("An exception occurred:", type(e).__name__, "–", e)
        exit(1)

    yield
    print("ending lifespan")


# app = FastAPI(dependencies=[Depends(get_settings)])
app = FastAPI(lifespan=lifespan)

get_bearer_token = HTTPBearer(auto_error=False)


def get_token(settings: Annotated[Settings, Depends(get_settings)], auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = auth.credentials
        if token is None:
            raise credentials_exception
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
        if token_data.username is None or token_data.username == "" or token_data.username != settings.APP_USER:
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
