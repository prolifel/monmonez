from typing import Union, Annotated
from fastapi import FastAPI, File, UploadFile, status, Response
import models
import util
import Statement
import pathlib
from fastapi.responses import FileResponse

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
