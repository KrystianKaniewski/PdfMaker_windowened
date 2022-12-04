import PyPDF2
import os

from tkinter import *
from tkinter import filedialog, Tk
from PIL import Image

def AddFiles():  # adding any files in three formats
    all_files = filedialog.askopenfilenames(initialdir="/pliki",
                                            filetypes=[('jpg', '*.jpg'),
                                                       ('png', '*.png'),
                                                       ('pdf', '*.pdf')])
    for file in all_files:
        allFiles.append(file)
    f = ""
    for file in allFiles:
        f = f + "\n" + file
    MyLabel1.config(text=f)

def dirMaker():
    out_file = os.path.expanduser('~') + "\Documents\PdfMaker"
    isExist = os.path.exists(out_file)
    if not isExist:
        os.makedirs(out_file)

def cancel():  # canceling operation by remove added files from list
    for i in allFiles:
        allFiles.remove(i)  ######################## cos nie tak
    MyLabel1.config(text="")
    entry.delete(0, END)
    entry.insert(0, "please, enter name of the output file here")

def nameCounter(name):
    out_file = os.path.expanduser('~') + "\Documents\PdfMaker\\" + name + ".pdf"
    isExist = os.path.exists(out_file)
    i = 1
    if isExist:
        while isExist:
            out_file = os.path.expanduser('~') + "\Documents\PdfMaker\\" + name + '_' + str(i) + '.pdf'
            i = i + 1
            isExist = os.path.exists(out_file)
    return out_file

def Convert():  # converting files into into one pdf file
    dirMaker()
    if not allFiles:
        cancel()
        MyLabel1.config(text="NO FILES TO CONVERT")
    else:
        if entry.get() == "please, enter name of the output file here":
            File = nameCounter('unknown')
        else:
            File = nameCounter(entry.get())
        pdf_r = open(File, 'wb')
        pdf_w = PyPDF2.PdfFileWriter()
        i = 0
        for file in allFiles:
            print(file)
            if file[-4:] == ".jpg" or file[-4:] == ".png":
                image1 = Image.open(file)
                im1 = image1.convert('RGB')
                num1 = str(i) + '.pdf'
                i = i + 1
                im1.save(num1)
                pdf_ra_ = open(num1, 'rb')
                pdf_ra = PyPDF2.PdfFileReader(pdf_ra_)
                pdf_w.addPage(pdf_ra.getPage(0))
                pdf_w.write(pdf_r)
                pdf_ra_.close()
                os.unlink(num1)
            elif file[-4:] == ".pdf":
                pdf_ra_ = open(file, 'rb')
                pdf_ra = PyPDF2.PdfFileReader(pdf_ra_)
                for pageN in range(pdf_ra.numPages):
                    page_obj = pdf_ra.getPage(pageN)
                    pdf_w.addPage(page_obj)
                pdf_w.write(pdf_r)
                pdf_ra_.close()
        pdf_r.close()
        cancel()
        MyLabel1.config(text="CONVERTING IS DONE!\nsaved in "+File)

if __name__ == "__main__":  # main structure of window
    allFiles = []

    window = Tk()
    window.title('PDF Maker')

    button_frame = Frame(window)
    button_frame.grid(row=2)
    entry_frame = Frame(window)
    entry_frame.grid(row=1)
    link_frame = Frame(window)
    link_frame.grid(row=0)

    entry = Entry(entry_frame, width=80)
    entry.insert(0, "please, enter name of the output file here")
    entry.pack()

    MyLabel1 = Label(link_frame)
    MyLabel1.pack()

    MyButton1 = Button(button_frame, text="Add Files", command=lambda: AddFiles(), padx=60, pady=20)
    MyButton2 = Button(button_frame, text="Convert", command=lambda: Convert(), padx=60, pady=20)
    MyButton3 = Button(button_frame, text="Cancel", command=lambda: cancel(), padx=60, pady=20)
    MyButton1.grid(row=1, column=0)
    MyButton2.grid(row=1, column=1)
    MyButton3.grid(row=1, column=2)

    window.mainloop()
