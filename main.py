import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
from PIL import ImageFilter
from PIL import Image
from PyQt5.QtGui import QPixmap
app = QApplication([])
windows10 = QWidget()
windows10.show()

workdir = ''
button_left = QPushButton('лево')
button_right = QPushButton('право')
button_mirror = QPushButton('зеркало')
button_rezkost = QPushButton('резкость')
button_L = QPushButton('ч/б')
button_papka = QPushButton('папка')
spisok = QListWidget()
paint = QLabel('CENSORED')

line1 = QHBoxLayout()
line2 = QVBoxLayout()
line3 = QVBoxLayout()
line4 = QHBoxLayout()

line4.addWidget(button_left)
line4.addWidget(button_right)
line4.addWidget(button_mirror)
line4.addWidget(button_rezkost)
line4.addWidget(button_L)
line2.addWidget(button_papka)
line2.addWidget(spisok)
line3.addWidget(paint)
line3.addLayout(line4)
line1.addLayout(line2)
line1.addLayout(line3)

windows10.setLayout(line1)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files,extensions):
    result = []
    for name in files:
        for ext in extensions:
            if name.endswith(ext):
                result.append(name)
    return result

def showFilenameslist():
    extensions = ['.jpg','.png', '.bmp', '.jpeg', '.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    spisok.clear()
    for name in filenames:
        spisok.addItem(name)


class ImageProcessor():
    def __init__(self):
        self.name = None
        self.image = None
        self.savedir = 'modified/'
        self.path = None
        self.image_path = None
    
    def loadImage(self,path,name):
        self.path = path
        self.name = name
        self.image_path = os.path.join(path,name)
        self.image = Image.open(self.image_path)
    
    def showImage(self):
        paint.hide()
        image_pixmap = QPixmap(self.image_path)
        image_pixmap = image_pixmap.scaled(paint.width(),paint.height(),Qt.KeepAspectRatio)
        paint.setPixmap(image_pixmap)
        paint.show()

    def saveImage(self):
        modif = os.path.join(self.path,self.savedir)
        if not (os.path.exists(modif) or os.path.isdir(modif)):
            os.mkdir(modif)
        modif = os.path.join(modif,self.name)
        self.image.save(modif)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        self.image_path = os.path.join(self.path,self.savedir)
        self.image_path = os.path.join(self.image_path,self.name)
        self.showImage()
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.image_path = os.path.join(self.path,self.savedir)
        self.image_path = os.path.join(self.image_path,self.name)
        self.showImage()
    def BLURED(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        self.image_path = os.path.join(self.path,self.savedir)
        self.image_path = os.path.join(self.image_path,self.name)
        self.showImage()
    def Left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        self.image_path = os.path.join(self.path,self.savedir)
        self.image_path = os.path.join(self.image_path,self.name)
        self.showImage()
    def Right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        self.image_path = os.path.join(self.path,self.savedir)
        self.image_path = os.path.join(self.image_path,self.name)
        self.showImage()
processor = ImageProcessor()

def showChosenImage():
    if spisok.currentRow() >= 0:
        filename = spisok.currentItem().text()
        processor.loadImage(workdir,filename)
        processor.showImage()

    


spisok.currentRowChanged.connect(showChosenImage)
button_papka.clicked.connect(showFilenameslist)
button_L.clicked.connect(processor.do_bw)
button_left.clicked.connect(processor.Left)
button_mirror.clicked.connect(processor.mirror)
button_rezkost.clicked.connect(processor.BLURED)
button_right.clicked.connect(processor.Right)

app.exec_()