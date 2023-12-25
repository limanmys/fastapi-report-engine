from fastapi import APIRouter
from fastapi.responses import FileResponse
import csv, time
from models.Request import ReportCreateRequest
from helpers.render import RenderClass
from helpers.docx2pdf import Converter

router = APIRouter()

# Crete PDF Report
@router.post("/pdf",summary="Creates a pdf report.", tags=["Report"])
def CreatePDFReport(body: ReportCreateRequest):
    timestamp = time.time()
    RenderClass.render(body, timestamp)
    return FileResponse(Converter.docx2pdf(timestamp))

# Crete CSV Report
@router.post("/csv",summary="Creates a csv report.", tags=["Report"])
def CreateCSVReport(body: ReportCreateRequest):
    filename = time.time()
    with open("./reports/%d.csv" % filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=body.Seperator)
        row = ["sep=" + body.Seperator]
        
        writer.writerow(row)
        writer.writerow([body.Header])
        writer.writerow(body.ReadableColumns)
        for data in body.Data:
            row = []
            for column in body.Columns:
                row.append(data[column])
            writer.writerow(row)

    return FileResponse("./reports/%d.csv" % filename)