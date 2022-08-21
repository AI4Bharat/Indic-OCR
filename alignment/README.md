# DocSynth.Alignment

Alignment is a package which provides text alignment features. 

There are two code files: 
* `generate_tsv.py`
    * input requires two files:
        * document PDF file
        * ground truth text file
    * the document is processed and OCR is performed to extract the text
    * this text is then matched with the ground truth text 
    * a TSV file is output containing 
        * words
        * bounding box information
        * aligned ground truth

* `word_align.py`
    * this file is used to generate visual representation of OCR accuracy
    * A green box is drawn around a word if its extracted accurately
    * A red box means not extracted accurately
    * input requires two files:
        * TSV file
        * document PDF file
    * the TSV file is processed and boxes are drawn on the PDF file
    * output is annotated PDF file with name `newdoc.pdf`