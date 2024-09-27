from PyQt5 import QtWidgets
import mysql.connector
import test
import update
import metod
import history
import sys

bd = mysql.connector.connect(
host='localhost',
user='root',
password='',
database='company'
)


cursor = bd.cursor()

class Company(QtWidgets.QMainWindow, test.Ui_MainWindow):
    def __init__(self):
        super(Company,self).__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.update_partner)
        self.pushButton_2.pressed.connect(self.material)
        self.pushButton_3.pressed.connect(self.histori)

        self.textEdit.setReadOnly(True)

        cursor.execute(f'SELECT * FROM partners_import ')
        x = cursor.fetchall()

        per = ""

        self.numder = 0
        self.sale = 0

        for r in x:
            self.sale = 0
            self.numder = 0

            cursor.execute(f'SELECT Amount_of_product FROM partner_products_import WHERE Partners_name = "{r[1]}"')
            y = cursor.fetchall()

            if len(y) != 0:
                for t in y:
                    self.numder += t[0]

            if 10000 <= self.numder & self.numder < 50000:
                self.sale = 5

            elif 50000 <= self.numder & self.numder < 300000:
                self.sale = 10

            elif self.numder >= 300000:
                self.sale = 15


            per += r[0] + " | " + r[1] + "                      " + str(self.sale) + "%\nДиректор: " + r[2] + "\n+7 " + r[4] + "\nрейтинг:" + str(r[7]) + "\n \n"


        self.textEdit.setText(per)

    def update_partner(self):
        self.ad = Update()
        self.ad.show()
        self.hide()

    def material(self):
        self.ad = Metod()
        self.ad.show()
        self.hide()

    def histori(self):
        self.ad = History()
        self.ad.show()
        self.hide()


class Update(QtWidgets.QMainWindow, update.Ui_MainWindow):
    def __init__(self):
        super(Update, self).__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.add_partner)
        self.pushButton_2.pressed.connect(self.edite_partner)
        self.pushButton_3.pressed.connect(self.del_partner)
        self.pushButton_4.pressed.connect(self.end)

        cursor.execute(f'SELECT Partners_name FROM partners_import')
        x = cursor.fetchall()
        for r in x:
            self.comboBox.addItem(r[0])

        self.comboBox.currentIndexChanged.connect(self.conclusion)



    def conclusion(self):
        Partners_name = self.comboBox.currentText()
        if len(Partners_name) != 0:
            cursor.execute(f'SELECT * FROM partners_import WHERE Partners_name = "{Partners_name}"')
            z = cursor.fetchall()

            self.lineEdit.setText(z[0][0])

            self.lineEdit_2.setText(z[0][1])
            self.lineEdit_3.setText(z[0][2])
            self.lineEdit_4.setText(z[0][3])
            self.lineEdit_5.setText(z[0][4])
            self.lineEdit_6.setText(z[0][5])
            self.lineEdit_7.setText(str(z[0][6]))
            self.spinBox.setValue(z[0][7])

            # cursor.execute(f'SELECT * FROM partner_products_import WHERE Partners_name = "{Partners_name}" ')
            # x = cursor.fetchall()

            # per = ""
            #
            # for r in x:
            #   per += "Наименование: " + "\n" + r[1] + "\n" + "Партнёр: " + "\n" + r[2] + "\n" + "Количество: " + "\n" + str(r[3]) + "\n" + "Дата: " + "\n" + r[4] + "\n" + ("-"*58) + "\n"
            #
            # self.textEdit.setText(per)




    def add_partner(self):
        Partners_type = self.lineEdit.text()
        Partners_name = self.lineEdit_2.text()
        Director = self.lineEdit_3.text()
        Partners_email = self.lineEdit_4.text()
        Partners_phone = self.lineEdit_5.text()
        Partners_legal_address = self.lineEdit_6.text()
        INN = self.lineEdit_7.text()
        Rating = self.spinBox.text()

        if Partners_type != "" and Partners_name != "" and Director != "" and Partners_email != "" and Partners_phone != "" and Partners_legal_address != "" and INN != "":

            cursor.execute(f'INSERT INTO partners_import VALUES ("{Partners_type}", "{Partners_name}", "{Director}", "{Partners_email}",  "{Partners_phone}", "{Partners_legal_address}", "{INN}","{Rating}")')
            bd.commit()

            self.comboBox.clear()

            cursor.execute(f'SELECT Partners_name FROM partners_import')
            x = cursor.fetchall()
            for r in x:
                self.comboBox.addItem(r[0])

            self.label_11.setText("Добавлено")

        else:
            # self.label_11.setText("неДобавлено")
            self.eBar = QtWidgets.QErrorMessage()
            self.eBar.setWindowTitle('Ошибка добавления')
            self.eBar.showMessage('Заполните все поля')
            # self.lineEdit.setStyleSheet("border-color: red;border-width: thick;")

    def del_partner(self):

        Partners_name = self.lineEdit_2.text()
        cursor.execute(f' DELETE FROM partners_import WHERE Partners_name = "{Partners_name}" ')
        bd.commit()
        self.comboBox.clear()

        cursor.execute(f'SELECT Partners_name FROM partners_import ')
        x = cursor.fetchall()

        for r in x:
            self.comboBox.addItem(r[0])

        self.label_11.setText("Удалено")

    def edite_partner(self):
        Partners_type = self.lineEdit.text()
        Partners_name = self.lineEdit_2.text()
        Director = self.lineEdit_3.text()
        Partners_email = self.lineEdit_4.text()
        Partners_phone = self.lineEdit_5.text()
        Partners_legal_address = self.lineEdit_6.text()
        INN = self.lineEdit_7.text()
        Rating = self.spinBox.text()

        cursor.execute(f'UPDATE partners_import SET Partners_type = "{Partners_type}", Director = "{Director}", Partners_email = "{Partners_email}", Partners_phone = "{Partners_phone}", Partners_legal_address = "{Partners_legal_address}", INN = "{INN}", Rating = "{Rating}" WHERE Partners_name = "{Partners_name}"')
        bd.commit()
        self.label_11.setText("Редактировано")

    def end(self):
        self.ad = Company()
        self.ad.show()
        self.hide()



class Metod(QtWidgets.QMainWindow, metod.Ui_MainWindow):
    def __init__(self):
        super(Metod,self).__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.rasch)
        self.pushButton_2.pressed.connect(self.end)

        cursor.execute(f'SELECT product_type FROM product_type_import')
        x = cursor.fetchall()
        for r in x:
            self.comboBox.addItem(r[0])

        cursor.execute(f'SELECT material_type FROM material_type_import')
        x = cursor.fetchall()
        for r in x:
            self.comboBox_2.addItem(r[0])
    #
    def rasch(self):

        cb1 = self.comboBox.currentText()
        cb2 = self.comboBox_2.currentText()
        cb3 = self.spinBox.text()


        cursor.execute(f'SELECT the_coefficient_of_the_product_type FROM product_type_import WHERE product_type = "{cb1}"')
        t1 = cursor.fetchall()
        cursor.execute(f'SELECT material_scrap_percentage FROM material_type_import WHERE material_type = "{cb2}"')
        t2 = cursor.fetchall()


        pert = int(cb3) * t1[0][0] / (1 - (t2[0][0] / 100))

        q, r = divmod(pert, 1)
        y = round(q) + bool(r)

        self.label_4.setText("Для такого количества " + cb1 + " нужно " + str(y) + " единиц материала: " + cb2)


    def end(self):
        self.ad = Company()
        self.ad.show()
        self.hide()


class History(QtWidgets.QMainWindow, history.Ui_MainWindow):
    def __init__(self):
        super(History, self).__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.end)

        self.textEdit.setReadOnly(True)

        cursor.execute(f'SELECT Partners_name FROM partners_import')
        x = cursor.fetchall()
        for r in x:
            self.comboBox.addItem(r[0])

        self.comboBox.currentIndexChanged.connect(self.conclusion)

    def conclusion(self):
        Partners_name = self.comboBox.currentText()
        if len(Partners_name) != 0:

            cursor.execute(f'SELECT * FROM partner_products_import WHERE Partners_name = "{Partners_name}" ')
            x = cursor.fetchall()

            per = ""

            for r in x:
                per += "Наименование: " + "\n" + r[1] + "\n" + "Партнёр: " + "\n" + r[
                    2] + "\n" + "Количество: " + "\n" + str(r[3]) + "\n" + "Дата: " + "\n" + r[4] + "\n" + (
                                   "-" * 58) + "\n"

            self.textEdit.setText(per)

    def end(self):
        self.ad = Company()
        self.ad.show()
        self.hide()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Company()
    myapp.show()
    sys.exit(app.exec())