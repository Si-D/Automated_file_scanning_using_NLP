#libraries

from __future__ import unicode_literals, print_function
import pytesseract
import spacy
import plac
import random
from pathlib import Path
from tqdm import tqdm
import fileinput
from pdf2image import convert_from_path 
import os 
from PIL import Image  
import csv
import sys 
from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import fileinput
import docx
from docx import Document
from docx2pdf import convert
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import timedelta
from datetime import datetime

#function to perform ocr

def ocr(path,nop=0):
    PDF_file = path
    pages = convert_from_path(PDF_file, 500) 
    image_counter = 1
    for page in pages: 
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG') 
        image_counter = image_counter + 1
    if nop!=0:
        filelimit = nop
    else:
        filelimit = image_counter-1
    outfile = "out_text.txt"
    f = open(outfile, "a") 
    output_text = ""
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
#         text = str(((pytesseract.image_to_string(Image.open(filename))))) 
        text = str(((pytesseract.image_to_string(filename)))) 
        text = text.replace('-\n', '')     
        output_text = output_text+text
        f.write(text) 
    f.close() 
    return output_text

    
#function to calculate date

def dat(da,years):
    import datetime
    from datetime import date
    from datetime import timedelta
    def getDate(da):
      date_entry = da
      day, month, year = map(int, date_entry.split('/'))
      return datetime.date(year, month, day)
    da = getDate(da)
    def addYears(d, years):
        try:
    #Return same day of the current year        
            return d.replace(year = d.year + years)
        except ValueError:
    #If not same day, it will return other, i.e.  February 29 to March 1 etc.        
            return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
    string=str(addYears(da,years))
    from datetime import datetime
    oldformat = string
    datetimeobject = datetime.strptime(oldformat,'%Y-%m-%d')
    newformat = datetimeobject.strftime('%d-%m-%Y')
    return newformat

#function to remove line ends in sentences

def space_text(text):
	text = text.strip()
	text = text.rstrip()
	text = text.lstrip()
	new_text = ""
	for i in range(len(text)):
	    if text[i] == '\n' and text[i+1] != '\n':
	            new_text = new_text + " "
	    else:
	        new_text = new_text + text[i]
	return new_text


#function to detect suite in given address

def suite(text):
    su = ''
    ind = text.find('#')
    for i in range(ind,len(text)):
        if text[i]!=" ":
            su = su + text[i]
        else:
            break
    return su


#fucntion to append predictions in dictionary

def pred2(paths,text):
    text = text.strip()
    new_text = text
    mod_path1=Path(paths[0])
    mod_path2=Path(paths[1])
    model = spacy.load(mod_path1)
    model1 = spacy.load(mod_path2)
    #model = nlp
    nlp1 = spacy.load("en_core_web_sm")
    doc1 = nlp1(new_text)
    doc = model(new_text.strip())
    doc2 = model1(new_text.strip())
    LN = []
    LA = []
    LC = []
    LP = []
    TN = []
    TA = []
    TC = []
    TP = []
    BA = []
    BC = []
    SU = []
    BP = []
    YE = []
    DA = []
    for ent in doc.ents:
        if ent.label_ == "LN":
            doc1 = nlp1(ent.text.rstrip())
            if(doc1.ents):
                if len(LN)==0 :#(doc1.ents[0].label_=="ORG"):
                    LN.append(ent.text)
        elif ent.label_ == "TN":
            doc1 = nlp1(ent.text.rstrip())
            if(doc1.ents):
                if len(TN)==0: #(doc1.ents[0].label_=="ORG") and:
                    TN.append(ent.text)
        elif ent.label_ == "LC":
            doc1 = nlp1(ent.text.rstrip())
            if(doc1.ents):
                if(doc1.ents[0].label_=="GPE") and len(LC)==0:
                    LC.append(ent.text)
        elif ent.label_ == "TC":
            doc1 = nlp1(ent.text.rstrip())
            if(doc1.ents):
                if(doc1.ents[0].label_=="GPE") and len(TC)==0:
                    TC.append(ent.text)
        elif ent.label_ == "LA":
            doc1 = nlp1(ent.text.rstrip())
            if(doc1.ents):
                if(doc1.ents[0].label_=="CARDINAL") and len(LA)==0:
                    LA.append(ent.text)
        elif ent.label_ == "TA":
            doc1 = nlp1(ent.text.rstrip())
            if(doc1.ents):
                if(doc1.ents[0].label_=="CARDINAL") and len(TA)==0:
                    TA.append(ent.text)
        elif ent.label_ == "LP":
    #         doc1 = nlp1(ent.text.rstrip())
    #         if(doc1.ents):
    #             #if(doc1.ents[0].label_=="CARDINAL") and 
    #             if len(doc1.ents[0].text)==6 and len(LP)==0:
    #                 LP.append(ent.text)
            if len(ent.text) == 6 and len(LP)==0:
                LP.append(ent.text)
        elif ent.label_ == "TP":
    #         doc1 = nlp1(ent.text.rstrip())
    #         print(len(doc1.ents[0].text),len(TP))
    #         if(doc1.ents):
    #             #if(doc1.ents[0].label_=="CARDINAL") and 
    #             if len(doc1.ents[0].text)==6 and len(TP)==0:
    #                 TP.append(ent.text)
            if len(ent.text) == 6 and len(TP)==0:
                TP.append(ent.text)
        elif ent.label_ == "BA":
            if len(BA) == 0 and len(SU)==0:
                ad = ent.text.replace("the space at\n","")
                su = suite(ad)
                BA.append(str(ad))
                SU.append(su)
                #print(ad)
        elif ent.label_ == "BC" and len(BC)==0:
            BC.append(ent.text.strip())
        elif ent.label_ == "BP" and len(BP)<=3 :
            BP.append(ent.text.strip())
        #print(ent.text.rstrip() , ent.label_)
    for ent in doc2.ents:
        if ent.label_ == "DA":
            DA.append(ent.text)
        elif ent.label_ == "YE":
            YE.append(int(ent.text.replace(" years","")))
        print(ent.text,ent.label_)
    #output={"ATenant":"Tenant   "+TN[0],"ALandlord":"Landlord    "+LN[0],"LAddress":"Address   "+LA[0]+LC[0]+LP[0],"TAddress":"Address   "+TA[0]+TC[0]+TP[0]}
    sqm = text.find("sqm")
    s = ""
    if sqm>0:
        sc = 0
        s = ""
        j = sqm-1
        while sc<2:
            if text[j] == ' ':
                sc=sc + 1
            else:
                s = s + text[j]
            j = j - 1
        s = s[::-1]
    else:
        s = "NA"
    area = s
    date = dat(DA[0],YE[0])
    #print(date)
    output = {
        "Tenant name": TN[0],
        "Tenant address": TA[0],
        "Tenant city":TC[0],
        "Tenant postal":BP[0],
        "Landlord name":  LN[0],
        "Landlord address":  LA[0],
        "Landlord city": LC[0],
        "Landlord postal": BP[1],
        "Building address": BA[0],
        "Building suite": SU[0],
        "Building city": BC[0],
        "Building postal": BP[2],
        "Date of commencement": DA[0],
        "Years": YE[0],
        "Date of expiry" : date,
        "Area(in sqm)":area
        
    }
#     for k in output:
#         output[k] = str(output[k]).strip()
#     output = []
#     output.append(LN)
#     output.append(LA)
#     output.append(LC)
#     output.append(LP)
#     output.append(TN)
#     output.append(TA)
#     output.append(TC)
#     output.append(TP)
#     for k in output:
#         print(k,output[k])
    return output


#fucntion to fill in csv file

def fill2(path,dic):
    fil = open(path,"w+")
    cs = csv.writer(fil)
    for i in dic:
        cs.writerow([i,dic[i]])
    fil.close()




root = Tkinter.Tk() 
root.geometry('500x500') 
T = Text(root, height = 10, width = 52) 
l = Label(root, text = "Automated text extraction") 
def open_file(): 
    file = askopenfile(mode ='r', filetypes =[('PDF Files', '*.pdf')]) 
    path = ""
    #print(file.name)
    for i in range(len(file.name)):
        if file.name[i] == '/':
            path = path + "\\"
        else:
            path = path + file.name[i]
    print(path)
    print("Applying OCR....")
    output_text = ocr(path)
    output_text = space_text(output_text)
    print("OCR completed....")
    print("Applying NLP....")
    paths = ["model_9","model_6"]
    output = pred2(paths,output_text)
    print("NLP completed...")
    print("CSV filling...")
    fill2("./outputs/sample2.csv",output)
    print("Process completed...")
    
    
#     if file is not None: 
#         content = file.read() 
#         print(content) 
l.pack()
btn = Button(root, text ='Open', command = lambda:open_file()) 
btn.pack(side = TOP, pady = 10) 
l.pack()
  
root.mainloop() 
