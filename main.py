
import sqlite3
import datetime
import time as ti
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import threading
import sys
import os
import notifypy


class mainwin(QWidget):
    def __init__(self):
        super().__init__()
        def appkill():
            os._exit(0)
        def appshow():
            self.show()
        def systemtray():
            tray = QSystemTrayIcon( self ,icon= QIcon('./a7f7a874fd.ico'))
            tray.setToolTip('Reminder...')
            menu =QMenu()
            exit = menu.addAction('Show Window')
            exit.triggered.connect(appshow)
            
            show = menu.addAction('Exit')
            show.triggered.connect(appkill)
            tray.setContextMenu(menu)
            
            tray.show()
        
        def show_info_messagebox(text):
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)


            msg.setText(text)


            msg.setWindowTitle('Reminder')


            msg.setStandardButtons(QMessageBox.Ok)


            msg.exec_()
        global breakecon 
        global stopcon   
        breakecon = False
        stopcon= False
        global ind
        ind=0
        def all_funcs():
            global stopcon 
            stopcon = True
            try:
                while True:
                    global ind
                    ind+=1
                    data = get_datas()

                    current_time = datetime.datetime.now().strftime('%I:%M %p')

                    for i in range(data.__len__()):
                        time = str((data[i][1]))

                        time = time.replace(" ", "")
                        current_time = current_time.replace(' ', '')
                        
                        if current_time[:1] == '0':
                            current_time = current_time[1:]

                        if time == current_time:
                            print('kj')
                            event = data[i][0]
                            event = event + f'   ( {current_time})'
                            threading.Thread(
                                target=lambda: notifition(event)).start()

                            ti.sleep(10)
                            threading.Thread(
                                target=lambda: notifition(event)).start()
                            ti.sleep(10)
                            threading.Thread(
                                target=lambda: notifition(event)).start()
                            ti.sleep(10)
                            threading.Thread(
                                target=lambda: notifition(event)).start()
                            ti.sleep(10)
                            threading.Thread(
                                target=lambda: notifition(event)).start()
                            ti.sleep(10)
                            threading.Thread(
                                target=lambda: notifition(event)).start()
                            ti.sleep(10)
                    ti.sleep(1)
                    global breakecon
                    if breakecon:

                        breakecon = False
                        break
                 
            except Exception as er:
                show_info_messagebox('Try again')

        def all_func_thrade():
            show_info_messagebox(
                'Started Successfully\nNow you can close the window')
            lable.setText('Runing...')
               
            threading.Thread(target=all_funcs).start()
          
        def loopstop():
            if stopcon == True:

                global breakecon
                breakecon = True
                lable.setText("Stoped")
        def notifition(msg):

            notify = notifypy.Notify()
            notify.title = 'Reminder'
            notify.message = msg
            notify.icon = './chat-text-dynamic-gradient.png'
            # notify.audio = './mixkit-orchestral-emergency-alarm-2974.wav'
            notify.send()

        def get_datas():

            con = sqlite3.connect('data.db')

            row = con.cursor()

            row.execute(f'''
                SELECT * FROM data
                ''')
            data = row.fetchall()

            con.close()
            return data

        def save_data(event, time):
            con = sqlite3.connect('data.db')

            row = con.cursor()

            row.execute(f'''
                INSERT INTO data VALUES('{event}' , '{time}')
                ''')
            con.commit()
            con.close()

        def delete_data(event):
            con = sqlite3.connect('data.db')

            row = con.cursor()

            row.execute(f'''
                DELETE FROM data
                ''')
            con.commit()
            con.close()
            addtable()

        def savedata():
            if eventlineedit.text() != '' and timelineedit.text() != '':

                save_data(eventlineedit.text(), timelineedit.text())
                addtable()
        def windowclose():
            
            self.setVisible(False)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(QtCore.QSize(450, 300))
        self.setWindowIcon(QIcon('./a7f7a874fd.png'))
        self.setWindowTitle('Reminder')
        boxlayoytfirst = QHBoxLayout(self)
        boxlayoyt = QVBoxLayout(self)
        lable = QLabel(self)
        lable.setStyleSheet('''QLabel{color: rgba(255 ,0 ,50)}''')
        lable.setText('Stoped')
        lable.setFont(QFont('Arial Rounded MT Bold' ,14))
        boxlayoyt.addWidget(lable , 0)

        boxlayoyt.addWidget(QLabel(text='Event'), 0)
        eventlineedit = QLineEdit(self)
        boxlayoyt.addWidget(eventlineedit)
        boxlayoyt.addWidget(QLabel(text='Time'), 0)
        timelineedit = QLineEdit(self)
        boxlayoyt.addWidget(timelineedit, 1)
        btn = QPushButton(self)

        btn.setIconSize(QtCore. QSize(25, 25))
        btn.setIcon(QIcon(QPixmap('./Save_perspective_matte_s.png')))
        btn.clicked.connect(savedata)

        boxlayoyt.addWidget(btn, 1)
        btn = QPushButton(self)
        btn.setIconSize(QtCore. QSize(30, 30))
        btn.setIcon(QIcon('./Rocket_perspective_matte_s.png'))
        btn.clicked.connect(all_func_thrade)
        boxlayoyt.addWidget(btn, 1)
        btn = QPushButton(self)
        btn.setIconSize(QtCore. QSize(30, 30))
        btn.setIcon(QIcon('./Basket_perspective_matte_s.png'))
        btn.clicked.connect(delete_data)
        boxlayoyt.addWidget(btn, 1)
        btn = QPushButton(self)
        btn.setIconSize(QtCore. QSize(30, 30))
        btn.setIcon(QIcon('./plus-dynamic-gradient.png'))
        btn.clicked.connect(windowclose)
        boxlayoyt.addWidget(btn, 1)
        btn = QPushButton(self)
        btn.setIconSize(QtCore. QSize(25, 25))
        btn.setIcon(QIcon('./stop-icon-vector-19829405.png'))
        btn.clicked.connect(loopstop)
        boxlayoyt.addWidget(btn, 1)

        table = QTableWidget(self)
        table.setColumnCount(2)

        table.setRowCount(get_datas().__len__())
        t = QTableWidgetItem()
        t.setText('Event')
        table.setHorizontalHeaderItem(0, t)
        t = QTableWidgetItem()
        t.setText('Time')
        tablewidth = 238
        table.setColumnWidth(0, tablewidth//2)
        table.setColumnWidth(1, tablewidth//2)
        print(tablewidth)

        def addtable():

            da = get_datas()
            table.setRowCount(da.__len__())
            for i in range(da.__len__()):

                print(i)
                d = da[i]
                print(d)
                t = QTableWidgetItem()
                t.setText(d[0])
                table.setItem(i, 0, t)
                t = QTableWidgetItem()
                t.setText(d[1])
                table.setItem(i, 1, t)
                table.update()
        table.setHorizontalHeaderItem(1, t)
        boxlayoytfirst.addLayout(boxlayoyt)
        boxlayoytfirst.addWidget(table)

        self.show()
        systemtray()
        threading.Thread(target=addtable).start()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    win = mainwin()
    os._exit(  app.exec_())
  
