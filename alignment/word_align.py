"""
description: visualises OCR validation through coloured bounding boxes
             for each word
                 - green: correct
                 - red: incorrect

arguments:   1) (.tsv) file,
             2) document (.pdf)

output:      document (.pdf)
"""


import pandas as pd
import fitz
import json 
import sys


# arguments from command line are read
# argument 1: tsv file 
# argument 2: PDF document file

args = sys.argv
tsv_filename, doc_filename = args[1], args[2]


# reading the files

df = pd.read_csv(tsv_filename, delimiter='\t')
doc = fitz.open(doc_filename)


# drawing green box if words match else red box using draw_rect
# reference: https://pymupdf.readthedocs.io/en/latest/page.html#Page.draw_rect

for i, row in df.iterrows():
    page = doc[row["pagenumber"]]
    x0, y0, x1, y1 = row[1:5]
    dim = page.rect

    xmax, ymax = dim.x1, dim.y1
    rect = fitz.Rect(x0, ymax-y1, x1, ymax-y0)

    color = 'green' if row["aligned_noise"] == row["aligned_gt"] else 'red'
    page.draw_rect(rect, fitz.utils.getColor(color))


# saving the annotated PDF document

newdoc = fitz.Document()
newdoc.insert_pdf(doc)
newdoc.save("newdoc.pdf")
