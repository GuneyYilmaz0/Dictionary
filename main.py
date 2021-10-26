import threading
import sys
import pyttsx3
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtWidgets import QMessageBox
from deep_translator import GoogleTranslator
from PySide6 import QtWidgets


class DictionaryGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AL-Dictionary")
        self.setWindowIcon(QIcon("Book.ico"))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QLabel()
        self.text.setText("Türkçe")
        self.text2 = QtWidgets.QLabel()
        self.text2.setText("English")
        self.textbox = QtWidgets.QTextEdit()
        self.textbox2 = QtWidgets.QTextEdit()
        self.text_en_tr = QtWidgets.QPushButton("English-Turkish")
        self.text_tr_en = QtWidgets.QPushButton("Turkish-English")
        self.speak = QtWidgets.QPushButton("Speak")

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.text2)
        self.layout.addWidget(self.textbox2)
        self.layout.addWidget(self.text_en_tr)
        self.layout.addWidget(self.text_tr_en)
        self.layout.addWidget(self.speak)

        self.text_en_tr.clicked.connect(self.english_to_turkish)
        self.text_tr_en.clicked.connect(self.turkish_to_english)
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)
        self.speak.clicked.connect(lambda: threading.Thread(
            target=speak, args=(self.textbox2.toPlainText(), engine), daemon=True
        ).start())

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, "Quit Dictionary", "Are you sure want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def english_to_turkish(self):
        try:
            arr = GoogleTranslator(source='en', target='tr').translate(self.textbox2.toPlainText())
            self.textbox.setText(arr)
        except:
            self.text2.setText("English - You must not leave the box blank")

    def turkish_to_english(self):
        try:
            arr = GoogleTranslator(source='tr', target='en').translate(self.textbox.toPlainText())
            self.textbox2.setText(arr)
        except:
            self.text.setText("Türkçe - Kutucuğu boş bırakmamalısın")


def speak(string, engine):
    try:
        engine.say(string)
        engine.runAndWait()
    except RuntimeError:
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle("fusion")

    widget = DictionaryGUI()
    widget.resize(500, 500)
    widget.show()

    sys.exit(app.exec())
