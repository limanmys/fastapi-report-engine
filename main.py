
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

@app.get("/templates",summary="Lists all templates.", tags=["Template"])
def ListTemplates():
    base_path = os.getcwd() + "/templates/"
    result = []

    for file in [f for f in os.listdir(base_path)]:
        res = dict()
        file_stats = os.stat(base_path+ file)
        res["name"] = file
        res["size"] = file_stats.st_size
        result.append(res)

    return result

@app.get("/templates/{name}",summary="Lists all templates.", tags=["Template"])
def ListTemplates(name: str):
    base_path = os.getcwd() + "/templates/" + name
    file_stats = os.stat(base_path)
    res = dict()
    res["name"] = name
    res["size"] = file_stats.st_size
    
    return res

@app.delete("/templates/{name}",summary="Lists all templates.", tags=["Template"])
def ListTemplates(name: str):
    os.remove(os.getcwd() + "/templates/" + name)
    return "Item deleted successfully."


@app.post("/templates", summary="Uploads new template.", tags=["Template"])
def SaveTemplate(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        name = file.filename.replace(" ", "_")
        name = file.filename.replace("-", "_")
       
        with open(name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        os.rename(name, "./templates/" + name)
    
    return {"message": f"Successfully uploaded {name}"}