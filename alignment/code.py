"""
description: performs OCR on given document PDF, 
             aligns OCR output with given ground truth,
             outputs TSV file containing 
                - extracted words
                - bounding box information
                - line, section and page number
                - aligned noise and ground truth

arguments:   1) document (.pdf),
             2) ground truth (.txt)

output:      (.tsv) file
"""


from genalog.text import anchor
import pandas as pd
import fitz
import json 
import sys

# arguments from command line are read
# argument 1: document pdf file 
# argument 2: ground truth file

args = sys.argv
doc_filename, ground_truth_filename = args[1], args[2]


# perform OCR on document pdf using PyMuPDF (https://pymupdf.readthedocs.io/en/latest/index.html)
# get_text("words") extracts words in the form (x0, y0, x1, y1, "word", block_no, line_no, word_no)
# reference: https://pymupdf.readthedocs.io/en/latest/textpage.html#TextPage.extractWORDS
# extract words and record corrosponding page number

doc = fitz.open(doc_filename)
words, wordpagemap = [], []

for i in range(len(doc)):
    page = doc[i] 
    curwords = page.get_text("words")
    words.extend(curwords)  
    wordpagemap += [i]*len(curwords)


# aggregate extracted words to a file
# noise represents OCR output

noise = " ".join(i[4] for i in words)
with open('noise.txt', 'w') as f:
    f.write(noise)


# read ground truth from provided file

with open(ground_truth_filename, encoding="utf8") as f:
    groud_truth = f.read()
  

# align ground truth with noise using Genalog
# reference: https://microsoft.github.io/genalog/docstring/genalog.text.html#genalog.text.anchor.align_w_anchor
# output is written to files for reference

aligned_gt, aligned_noise = anchor.align_w_anchor(ground_truth, noise)

with open('aligned_gt.txt', 'w') as f:
    f.write(aligned_gt)
 
with open('aligned_noise.txt', 'w') as f:
    f.write(aligned_noise)


# re-aligning aligned_gt words corrsponding to each word from aligned_noise
# algorithm: maintain two pointers for gt and noise each
#            using noise pointer traverse aligned_noise until space occurs
#            meanwhile record corrosponding letters from aligned_gt using gt pointer

aligned_noise_words, aligned_gt_words = aligned_noise.split(), []
cur_gt, max_i = "", len(aligned_noise)-1

for i, val in enumerate(aligned_noise):
    if val == " " or i == max_i: 
        aligned_gt_words.append(cur_gt)
        cur_gt = ""
    else:
        cur_gt += aligned_gt[i]


# insert the records to a pandas dataframe and then to a tsv file
# records: "x0", "y0", "x1", "y1", "noise", "blocknumber", "linenumber", "wordnumber", 
#          "pagenumber", "aligned_noise", "aligned_gt"

op = []

for i in range(len(words)):
    op.append(list(map(str, words[i])) + [wordpagemap[i], aligned_noise_words[i], aligned_gt_words[i]])

op = pd.DataFrame(op, columns=["x0", "y0", "x1", "y1", "noise", "blocknumber", "linenumber", "wordnumber", "pagenumber", "aligned_noise", "aligned_gt"])
op.to_csv("op.tsv", sep="\t")

