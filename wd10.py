from docx import Document

doc = Document()
style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
doc.add_paragraph('Some text\n')
doc.save('test9.docx')