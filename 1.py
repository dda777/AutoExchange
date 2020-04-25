from PyQt5 import Qt
import random

class WorkThread(Qt.QThread):
    ''' Потоковая задача WorkThread со своим окном. '''

    threadSignal = Qt.pyqtSignal(int)     

    def __init__(self, startParm):
        super().__init__()
        self.startParm = startParm

    def run(self, *args, **kwargs):
        while self.startParm != 99:
            Qt.QThread.msleep(200)
            self.startParm += 1
            # Излючаем сигнал и передаем аргументы подключенному слоту
            self.threadSignal.emit(self.startParm)   


class WorkThreadMain(Qt.QThread):
    ''' Потоковая задача WorkThreadMain без своего окна. '''

    threadSignalMain = Qt.pyqtSignal(int)

    def __init__(self, startParm):
        super().__init__()
        self.startParm = startParm

    def run(self, *args, **kwargs):
        while True:
            Qt.QThread.msleep(1000)
            self.startParm += 1
            self.threadSignalMain.emit(self.startParm)


class MsgBox(Qt.QDialog):
    """ Класс инициализации окна для визуализации потока WorkThread
        и кнопка для закрытия потокового окна, если поток остановлен! """

    def __init__(self):
        super().__init__()
        self.setGeometry(900, 65, 400, 80)
        self.setWindowTitle('MsgBox для WorkThread')

        self.label = Qt.QLabel("")
        self.close_btn = Qt.QPushButton("Close поток WorkThread")
        # закроет окно, если поток остановлен
        self.close_btn.clicked.connect(self.close)        

        layout = Qt.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.close_btn)


class MainWindow(Qt.QWidget):    
    ''' Главное окно. В методе __init__:
    - объявили все виджеты, установили валидацию    
    - привязали нажатие кнопок к сигналам для вызова нужных слотов 
    - создали экземпляр дополнительного окна '''

    def __init__(self):
        super().__init__()
        self.setGeometry(540, 65, 320, 200)
        self.setWindowTitle('MainWindow')

        self.labelMain = Qt.QLabel("Результат потоковой задачи WorkThreadMain: ")
        self.labelThread = Qt.QLabel("Результат Потоковой задачи WorkThread: ")
        validator = Qt.QIntValidator(1, 999, self)
        validator.setBottom(1)
        self.lineEdit = Qt.QLineEdit()
        self.lineEdit.setPlaceholderText("Начильный параметр для потоковой задачи WorkThread")
        # self.lineEdit будет принимать только целые числа от 1 до 999 
        self.lineEdit.setValidator(validator)    
        self.btn = Qt.QPushButton("Start поток WorkThread")
        self.btn.clicked.connect(self.on_btn)
        self.btnMain = Qt.QPushButton("Запустить поток WorkThreadMain")
        self.btnMain.clicked.connect(self.on_btnMain)

        layout = Qt.QVBoxLayout(self) 
        layout.addWidget(self.labelMain)
        layout.addWidget(self.labelThread)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.btn)
        layout.addWidget(self.btnMain)

        self.msg = MsgBox()  
        self.thread     = None
        self.threadMain = None  

    def on_btn(self):
        ''' Запуск или Останов дополнительного Потока-WorkThread из главнонго окна '''

        # Входные параметры для передачи в поток, если не заданы, то передаем дефолтные `0`
        startParm = int(self.lineEdit.text()) if self.lineEdit.text() else 0 

        if self.thread is None:                     
            self.thread = WorkThread(startParm)     # Создаем поток, передакм параметры
            self.thread.threadSignal.connect(self.on_threadSignal)
            # Этот сигнал испускается из связанного потока непосредственно перед его завершением.
            self.thread.finished.connect(self.onFinished)  
            self.thread.start()                            # Стартуем поток

            self.btn.setText("Stop поток WorkThread")      # Меняем название кнопки
            self.lineEdit.hide()                           # Прячем виджет ввода пареметров
        else:
            self.thread.terminate()                        # Завершает выполнение потока
            self.thread = None
            self.btn.setText("Start поток WorkThread")
            self.lineEdit.show()

    def onFinished(self):
        print('close_btn.click()')
        self.msg.close_btn.click()
        self.thread = None
        self.btn.setText("Start поток WorkThread")
        self.lineEdit.show()

    def on_threadSignal(self, value):
        ''' Визуализация потоковых данных-WorkThread в основном окне. '''

        self.msg.label.setText(str(value))
        self.labelThread.setText("Результат Потоковой задачи WorkThread: {}".format(str(value)))

        # Восстанавливаем визуализацию потокового окна, если его закрыли. Поток работает.
        if not self.msg.isVisible():        
            self.msg.show()

    def on_btnMain(self):
        ''' Запуск или Останов Потока-WorkThreadMain '''

        cM = random.randrange(1, 100)
        if self.threadMain is None:
            self.threadMain = WorkThreadMain(cM)
            self.threadMain.threadSignalMain.connect(self.on_threadSignalMain)
            self.threadMain.start()
            self.btnMain.setText("Стоп поток WorkThreadMain")
        else:
            self.threadMain.terminate()         
            self.threadMain = None
            self.btnMain.setText("Старт поток WorkThreadMain")

    def on_threadSignalMain(self, value):
        ''' Визуализация потоковых данных WorkThreadMain в основном окне. '''

        self.labelMain.setText("Результат потоковой задачи WorkThreadMain: " + str(value)) 


if __name__ == '__main__':
    import sys
    app = Qt.QApplication(sys.argv)
    mw  = MainWindow()
    mw.show()
    sys.exit(app.exec_()) 