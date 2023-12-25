from fastapi import UploadFile, File, APIRouter
from helpers.docx2pdf import Converter
import os, base64
from pdf2image import convert_from_path

router = APIRouter()

# Lists all templates
@router.get("/",summary="Lists all templates.", tags=["Template"])
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
@router.get("/{name}",summary="Get single template.", tags=["Template"])
def GetTemplate(name: str):
    base_path = os.getcwd() + "/templates/" + name
    file_stats = os.stat(base_path)
    res = dict()
    res["name"] = name
    res["size"] = file_stats.st_size
    
    return res

# Get template's preview
@router.get("/preview/{name}",summary="Get template's preview.", tags=["Template"])
def PreviewTemplate(name: str):
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
@router.delete("/{name}",summary="Deletes a template.", tags=["Template"])
def DeleteTemplate(name: str):
    os.remove(os.getcwd() + "/templates/" + name)
    return "Item deleted successfully."

# Upload new template
@router.post("/", summary="Uploads new template.", tags=["Template"])
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