from queue import Queue
from PyQt6.QtCore import QThread, QObject, pyqtSignal, Qt, pyqtSlot
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QFont
from client.gui.client_window import Ui_MainWindow


class Receiver(QObject):
    got_message = pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client

    def receive(self):
        while message := self.client.receive_message():
            self.got_message.emit()


class MainClientGui(Ui_MainWindow):
    def __init__(self, db, client):
        super().__init__()
        self.db = db
        self.client = client
        self.setupUi()
        self.listView.doubleClicked.connect(self.select_chat)
        self.update_users()

    @pyqtSlot()
    def incomming_message(self):
        self.update_users()
        self.update_messages()

    def update_users(self):
        users = self.db.get_users()
        self.users_model = QStandardItemModel()
        for user in users:
            active = "🍉" if user.is_active else "💀"
            contact = "👤" if user.is_contact else " "
            username = QStandardItem(f"{active} {user.username} {contact}")
            username.setEditable(False)
            self.users_model.appendRow(username)
        self.listView.setModel(self.users_model)

    def select_chat(self):
        self.chat = self.listView.currentIndex().data()[2:-2]
        self.label_2.setText(f"{self.chat}")
        self.update_messages()

    def update_messages(self):
        contact = self.label_2.text()
        messages = self.db.get_messages(contact)
        self.messages.clear()
        for message in messages:
            text = QStandardItem(f"{message.message}")
            date = QStandardItem(f"{message.date.replace(microsecond=0)}")
            date.setFont(QFont("Helvetica", 6))
            for row in (text, date):
                row.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft
                    if message.recieved == True
                    else Qt.AlignmentFlag.AlignRight
                )
                self.messages.appendRow(row)

    def start_messaging(self):
        self.receiver = Receiver(self.client)
        self.receiver.got_message.connect(self.incomming_message)
        self.recv_thread = QThread()
        self.receiver.moveToThread(self.recv_thread)
        self.recv_thread.started.connect(self.receiver.receive)
        self.recv_thread.start()
