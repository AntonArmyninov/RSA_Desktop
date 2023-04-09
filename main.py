from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog
from genKey import gen_key
import sys
import encrypt

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("RSA шифрование")
        self.setGeometry(300, 250, 350, 200)

        self.text_edit=QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.createMenuBar()
        self.installKey()


    def installKey(self):
        gen_key()


    def createMenuBar(self):
        self.menuBar =QMenuBar(self)
        self.setMenuBar(self.menuBar)
        fileMenu = QMenu("&Файл", self)
        self.menuBar.addMenu(fileMenu)


        open_file = fileMenu.addAction("Открыть", self.action_clicked)
        save_file = fileMenu.addAction("Сохранить", self.action_clicked)
        encrypt_file = fileMenu.addAction("Зашифровать",self.action_clicked)
        decrypt_file = fileMenu.addAction("Дешифровать",self.action_clicked)
        key_gen = fileMenu.addAction("Сгенерировать ключ", self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()
        if action.text() == "Открыть":
            print("open")
            fname = QFileDialog.getOpenFileName(self)[0]
            try:
                f = open(fname, 'r')
                with f:
                    data = f.read()
                    self.text_edit.setText(data)
                    f.close()
            except FileNotFoundError:
                print("Не выбран файл")

        elif action.text() == "Сохранить":
            print("save")
            fname=QFileDialog.getSaveFileName(self)[0]
            try:
                f = open(fname, 'w')
                #берем текст
                text = self.text_edit.toPlainText()
                f.write(text)
                f.close()
            except FileNotFoundError:
                print("Не выбран файл")

        elif action.text() == "Зашифровать":
            #нужно передать значения из эдитора в файл data.pem
            fname = 'data.pem'
            f = open(fname, 'w')
            # берем текст
            text = self.text_edit.toPlainText()
            f.write(text)
            f.close()
            publicKeyFile = 'public.pem'
            encryptedFile = encrypt.encrypt_file(fname, publicKeyFile)
            try:
                f = open(encryptedFile, 'r')
                with f:
                    data = f.read()
                    self.text_edit.setText(data)
                    f.close()
            except UnicodeDecodeError:
                print("Ошибка кодировки попробуй еще раз!")

        elif action.text() == "Дешифровать":
            decryptFile = 'data_encrypted.pem'
            privateKeyFile = 'private.pem'
            try:
                decryptedFile = encrypt.decrypt_file(decryptFile, privateKeyFile)
                f = open(decryptedFile, 'r')
                with f:
                    data = f.read()
                    self.text_edit.setText(data)
                    f.close()
            except ValueError:
                print("Не выбран файл")

        elif action.text() == "Сгенерировать ключ":
            gen_key()



def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ =="__main__":
    application()