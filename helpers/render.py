from docxtpl import DocxTemplate

class RenderClass():
    def render( body):
        template = DocxTemplate("./templates/%s" % body.TemplateID)
        template.render(body)    
        template.save("./results/%s.docx" % body.TemplateID)
