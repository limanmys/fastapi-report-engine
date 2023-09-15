
from fastapi import FastAPI
from docxtpl import DocxTemplate
from models.Request import ReportCreateRequest
import os
import subprocess

app = FastAPI()

@app.post("/pdf",summary="Creates a pdf report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    template = DocxTemplate("dynamic_table.docx")
    template.render(body)    
    template.save("dynamic_table_out.docx")

    os.system('soffice --headless --norestore --writer --convert-to pdf ./dynamic_table_out.docx')

    return "fatih arslan tugay"
