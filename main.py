from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from models.Request import ReportCreateRequest
from helpers.render import RenderClass
from helpers.docx2pdf import Converter
import uvicorn
import os, base64
import csv, time
from pdf2image import convert_from_path


app = FastAPI()

@app.post("/pdf",summary="Creates a pdf report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    RenderClass.render(body)
    return FileResponse(Converter.docx2pdf(body.TemplateID))

@app.post("/csv",summary="Creates a csv report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    filename = time.time()
    with open("./reports/%d.csv" % filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=body.Seperator)
        row = ["sep=" + body.Seperator]
        
        writer.writerow(row)
        writer.writerow(body.Header)
        writer.writerow(body.ReadableColumns)
        for data in body.Data:
            row = []
            for column in body.Columns:
                row.append(data[column])
            writer.writerow(row)

    return FileResponse("./reports/%d.csv" % filename)

# Lists all templates
@app.get("/templates",summary="Lists all templates.", tags=["Template"])
def ListTemplates():
    base_path = os.getcwd() + "/templates/"
    result = []

    for file in [f for f in os.listdir(base_path)]:
        res = dict()
        file_stats = os.stat(base_path+ file)
        if os.path.splitext(file)[1] == ".docx":
            res["name"] = file
            res["size"] = file_stats.st_size
            result.append(res)

    return result

# Get single template
@app.get("/templates/{name}",summary="Get single template.", tags=["Template"])
def ListTemplates(name: str):
    base_path = os.getcwd() + "/templates/" + name
    file_stats = os.stat(base_path)
    res = dict()
    res["name"] = name
    res["size"] = file_stats.st_size
    
    return res

# Get template's preview
@app.get("/templates/preview/{name}",summary="Get template's preview.", tags=["Template"])
def TemplatePreview(name: str):
    base_path = os.getcwd() + "/templates/" + name
    pdf_path = Converter.docx2preview(base_path)
    pdf_path = pdf_path.replace("docx", "pdf")
    
    pages = convert_from_path(pdf_path)
    name = name.replace(".docx", ".png")
    pages[0].save(name, 'png')
    with open(name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    response = dict()
    response["encoded"] = encoded_string
    return response

# Delete template
@app.delete("/templates/{name}",summary="Deletes a template.", tags=["Template"])
def ListTemplates(name: str):
    os.remove(os.getcwd() + "/templates/" + name)
    return "Item deleted successfully."

# Upload new template
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