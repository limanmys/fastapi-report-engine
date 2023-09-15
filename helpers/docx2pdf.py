import os

class Converter():
    def docx2pdf(file_name):
        docx_file = "./results/" + file_name + ".docx"
        os.system('soffice --headless --norestore --writer --convert-to pdf ./%s --outdir %s' % (docx_file, "./reports"))
        os.remove(docx_file)

        return "./reports/" + file_name + ".pdf"
