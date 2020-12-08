from docx import Document
from docx2pdf import convert

doc = Document("hello.docx")
Dictionary = {"NER": "BERT"}
for i in Dictionary:
    for p in doc.paragraphs:
        if p.text.find(i)>=0:
            p.text=p.text.replace(i,Dictionary[i])
#save changed document
doc.save('./test.docx')

convert("test.docx")
convert("test.docx", "output.pdf")

