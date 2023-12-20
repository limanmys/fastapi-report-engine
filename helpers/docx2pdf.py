import os

class Converter():
    def docx2pdf(file_name):
        docx_file = "./results/%d.csv" % file_name
        os.system('soffice --headless --norestore --writer --convert-to pdf ./%s --outdir %s' % (docx_file, "./reports"))
        os.remove(docx_file)

        return "./reports/%s.pdf" % docx_file
    
    def docx2preview(file_name):
        os.system('soffice --headless --norestore --writer --convert-to pdf %s --outdir %s' % (file_name, "./templates"))
        return file_name
