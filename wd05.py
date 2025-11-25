from docx import Document
from docx.shared import Cm
doc = Document()
t = doc.add_table(rows=2, cols=3)
t.style = doc.styles['Table Grid']
rows = t.rows[0].cells
rows[0].text = 'a'
rows[1].text = 'b'
rows[2].text = 'c'
rows1 = t.rows[1].cells
rows1[0].text = 'd'
rows1[1].text = 'e'
rows1[2].text = 'f'
rows2 = t.add_row().cells
t.add_column(width=Cm(2))
doc.save('test5.docx')