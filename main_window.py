from PyQt6.QtWidgets import QMainWindow, QWidget, QListView, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import QStringListModel
from database import Database
from form_window import FormWindow
class MainWindow(QMainWindow):   
    def __init__(self):
        super().__init__()
        self.windowTitle = "Главная"
        self.resize(800,600)

        list_widget = QWidget()
        self.list_view = QListView(list_widget)
        self.list_view.setModel(self.get_list_model_news())
        self.list_view.resize(800,600)

        self.del_button = QPushButton("Удалить")
        self.del_button.clicked.connect(self.del_new)
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_new)
        self.edit_button = QPushButton("Изменить")
        self.edit_button.clicked.connect(self.edit_new)
        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.update_list_view_news)

        buttons = QHBoxLayout()
        buttons.addWidget(self.add_button)
        buttons.addWidget(self.del_button)
        buttons.addWidget(self.edit_button)
        buttons.addWidget(self.update_button)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons)

        layout = QVBoxLayout()
        layout.addWidget(buttons_widget)
        layout.addWidget(list_widget)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def get_list_model_news(self):
        list_model = QStringListModel()
        list_model.setStringList(self.get_news())
        return list_model

    def update_list_view_news(self):
        self.list_view.setModel(self.get_list_model_news())    

    def get_news(self):
        db = Database()
        result_raw = db.get_news()
        result = []
        for r in result_raw:
            result.append(str(r["id"]) + ": " + r["name"])
        return result

    def del_new(self, id):
        db = Database()
        indexes = self.list_view.selectedIndexes()

        for index in indexes:
            id = str(index.data()).split(":")[0]
            db.del_new(id)
        self.update_list_view_news()

    def add_new(self):
        form_window = FormWindow(self)
        if form_window.exec() == 1:
            db = Database()
            db.add_new(form_window.name_text.text())
            self.update_list_view_news()
    def edit_new(self):
        if len(self.list_view.selectedIndexes()) <= 0: return
        form_window = FormWindow(self, str(self.list_view.selectedIndexes()[0].data()))
        if form_window.exec() == 1:
            db = Database()
            db.edit_new(form_window.name_text.text(), form_window.id)
            self.update_list_view_news()


