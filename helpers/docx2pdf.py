import os

class Converter():
    def docx2pdf(timestamp):
        template_filename = "./results/%d.docx" % timestamp
        os.system('soffice --headless --norestore --writer --convert-to pdf ./%s --outdir %s' % (template_filename, "./reports"))
        report_filename = "./reports/%d.pdf" % timestamp
        return report_filename
    
    def docx2preview(file_name):
        os.system('soffice --headless --norestore --writer --convert-to pdf %s --outdir %s' % (file_name, "./templates"))
        return file_name
