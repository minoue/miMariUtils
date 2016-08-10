from PySide import QtGui, QtCore
import sys
import os


class TextViewer(QtGui.QGraphicsView):
    """Dragable viewer for text generator"""

    def __init__(self, parent=None):
        super(TextViewer, self).__init__(parent)
        self.textScene = QtGui.QGraphicsScene()
        self.setScene(self.textScene)

        self.home = os.path.expanduser("~")

    def initItem(self, pixmap):
        self.scene().clear()
        self.pixmapItem = QtGui.QGraphicsPixmapItem(pixmap)
        self.scene().addItem(self.pixmapItem)

        self.pixmapRect = self.pixmapItem.boundingRect()
        self.scene().setSceneRect(self.pixmapRect)

        self.pathData = os.path.join(self.home, "temp.png")
        self.pixmapData = pixmap

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            try:
                data = QtCore.QMimeData()
                data.setData('text/plain', self.pathData)
                data.setUrls([QtCore.QUrl.fromLocalFile(self.pathData)])

                drag = QtGui.QDrag(self)
                drag.setMimeData(data)
                drag.setPixmap(self.pixmapData)
                drag.exec_()
            except AttributeError:
                """if text image are not generated yet, do nothing"""
                pass
        else:
            pass


class TextGenerator(QtGui.QDialog):

    def __init__(self, parent=None):
        super(TextGenerator, self).__init__(parent)

        # Change this path based on your environment
        self.textImagePath = os.path.join(os.path.expanduser("~"), "temp.png")
        self.setWindowTitle("Text Generator")
        self.setWindowFlags(QtCore.Qt.Window)

        self.resize(800, 400)

        textLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)

        # Text tab
        self.textViewer = TextViewer()
        self.textLE = QtGui.QLineEdit()
        self.textLE.setFocus()
        self.fontComboBox = QtGui.QFontComboBox()
        self.weightCB = QtGui.QComboBox()
        self.weightCB.addItems(['Normal', 'Bold', 'Light', 'Italic'])
        self.weightCB.currentIndexChanged.connect(self.updateTextViewer)
        self.sizeSpinBox = QtGui.QDoubleSpinBox()
        self.sizeSpinBox.setMinimum(1.0)
        self.sizeSpinBox.setMaximum(500.0)
        self.sizeSpinBox.setValue(100.0)
        self.textLE.textChanged.connect(self.updateTextViewer)
        self.fontComboBox.currentFontChanged.connect(self.updateTextViewer)
        self.sizeSpinBox.valueChanged.connect(self.updateTextViewer)
        formLayout = QtGui.QFormLayout()
        formLayout.addRow(self.tr("&Text:"), self.textLE)
        formLayout.addRow(self.tr("&Font:"), self.fontComboBox)
        formLayout.addRow(self.tr("Font &Size:"), self.sizeSpinBox)
        usage = ("Drag image to Mari viewport/Imagemanager\n"
                 "If you want to save image, drag it to wherever you want\n"
                 "(for example, Desktop, file browser, etc...)")
        usageLabel = QtGui.QLabel()
        usageLabel.setText(usage)
        textLayout.addWidget(self.textViewer)
        textLayout.addWidget(self.textLE)
        textLayout.addWidget(self.fontComboBox)
        textLayout.addWidget(self.weightCB)
        textLayout.addWidget(self.sizeSpinBox)
        textLayout.addWidget(usageLabel)

        self.setLayout(textLayout)
        # Text tab end

    def updateTextViewer(self):
        font = QtGui.QFont(self.fontComboBox.currentFont())
        font.setPointSizeF(self.sizeSpinBox.value())
        metrics = QtGui.QFontMetricsF(font)

        weight = self.weightCB.currentText()
        if weight == "Normal":
            font.setWeight(50)
        elif weight == "Bold":
            font.setWeight(75)
        elif weight == "Light":
            font.setWeight(25)
        elif weight == "Italic":
            font.setItalic(True)
        else:
            pass

        text = unicode(self.textLE.text())
        if not text:
            return

        rect = metrics.boundingRect(text)
        position = -rect.topLeft()

        pixmap = QtGui.QPixmap(rect.width(), rect.height())
        pixmap.fill(QtCore.Qt.white)

        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.setFont(font)
        painter.drawText(position, text)
        painter.end()

        self.textViewer.initItem(pixmap)
        self.textViewer.pixmapData.save(self.textImagePath)

    def createUI(self):
        self.view = TextViewer()

    def layoutUI(self):

        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        layout.addWidget(self.view)

        self.setLayout(layout)


def main():
    app = QtGui.QApplication(sys.argv)
    textWindow = TextGenerator()
    textWindow.show()
    textWindow.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
