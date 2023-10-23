from docxtpl import DocxTemplate

class RenderClass():
    def render(body):
        template = DocxTemplate("./templates/%s" % body.TemplateID)
        for idx,item in enumerate(body.Data):
            item["idx"] = idx
            body.Data[idx] = item
        template.render(body)    
        template.save("./results/%s.docx" % body.TemplateID)
