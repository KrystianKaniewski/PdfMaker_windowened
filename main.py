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
    file = ""
    for f in all_files:
        file = file + "\n" + f
        allFiles.append(f)

    MyLabel1.config(text=file)


def cancel():  # canceling operation by remove added files from list
    for i in allFiles:
        allFiles.remove(i)
    MyLabel1.config(text="")


def ConvertFromImg():  # converting image files into into one pdf file
    if not allFiles:
        cancel()
        MyLabel1.config(text="NO FILES TO CONVERT")
    else:
        if entry.get() == "":
            pdf_r = open("unknown.pdf", 'wb')
        else:
            pdf_r = open(entry.get() + ".pdf", 'wb')
        pdf_w = PyPDF2.PdfFileWriter()
        i = 0
        for file in allFiles:
            print(file)
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
        pdf_r.close()
        cancel()
        MyLabel1.config(text="CONVERTING IS DONE!")


def ConvertFromPDFS():  # converting few pdf files into one pdf file
    if not allFiles:
        cancel()
        MyLabel1.config(text="NO FILES TO CONVERT")
    else:
        if entry.get() == "":
            pdf_r = open("unknown.pdf", 'wb')
        else:
            pdf_r = open(entry.get() + ".pdf", 'wb')
        pdf_w = PyPDF2.PdfFileWriter()
        for file in allFiles:
            print(file)
            pdf_ra_ = open(file, 'rb')
            pdf_ra = PyPDF2.PdfFileReader(pdf_ra_)
            for pageN in range(pdf_ra.numPages):
                page_obj = pdf_ra.getPage(pageN)
                pdf_w.addPage(page_obj)
            pdf_w.write(pdf_r)
            pdf_ra_.close()
        pdf_r.close()
        cancel()
        MyLabel1.config(text="CONVERTING IS DONE!")


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
    entry.pack()

    MyLabel1 = Label(link_frame)
    MyLabel1.pack()

    MyButton1 = Button(button_frame, text="Add Files", command=lambda: AddFiles(), padx=20, pady=20)
    MyButton2 = Button(button_frame, text="Convert(Img->pdf)", command=lambda: ConvertFromImg(), padx=20, pady=20)
    MyButton3 = Button(button_frame, text="Convert(pdfs->pdf)", command=lambda: ConvertFromPDFS(), padx=20, pady=20)
    MyButton4 = Button(button_frame, text="Cancel", command=lambda: cancel(), padx=20, pady=20)
    MyButton1.grid(row=1, column=0)
    MyButton2.grid(row=1, column=1)
    MyButton3.grid(row=1, column=2)
    MyButton4.grid(row=1, column=3)

    window.mainloop()
