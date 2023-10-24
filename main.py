from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from models.Request import ReportCreateRequest
from helpers.render import RenderClass
from helpers.docx2pdf import Converter
import uvicorn
import os
import csv, time

app = FastAPI()

@app.post("/pdf",summary="Creates a pdf report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    RenderClass.render(body)
    return FileResponse(Converter.docx2pdf(body.TemplateID))

@app.post("/csv",summary="Creates a csv report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    filename = time.time()
    with open("./reports/%d.csv" % filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(body.Columns)

        for data in body.Data:
            row = []
            for column in body.Columns:
                row.append(data[column])
            writer.writerow(row)

    return FileResponse("./reports/%d.csv" % filename)

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

@app.delete("/templates/{name}",summary="Deletes a template.", tags=["Template"])
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

def serve():
    """Serve the web application."""
    uvicorn.run(app, port=8001, host='0.0.0.0')

if __name__ == "__main__":
    serve()