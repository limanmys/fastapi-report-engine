
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from models.Request import ReportCreateRequest
from helpers.render import RenderClass
from helpers.docx2pdf import Converter
import uuid
import os

app = FastAPI()

@app.post("/pdf",summary="Creates a pdf report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    RenderClass.render(body)
    return FileResponse(Converter.docx2pdf(body.TemplateID))


@app.post("/templates", summary="")
def SaveTemplate(file: UploadFile = File(...)):
    try:
        template_id = uuid.uuid4()
        contents = file.file.read()
        str_template_id = str(template_id)
        
        with open(str_template_id, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        os.rename(str_template_id, "./templates/" + str_template_id)
    
    return {"message": f"Successfully uploaded {file.filename}"}