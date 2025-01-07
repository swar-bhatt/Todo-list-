from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QListWidget,
    QWidget, QMessageBox, QInputDialog, QHBoxLayout, QComboBox, QListWidgetItem
)
from PyQt5.QtCore import Qt
import sys
import json

class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 400, 600)

        # Main Layout
        self.layout = QVBoxLayout()

        # Category Selector
        self.category_selector = QComboBox()
        self.category_selector.addItems(["All", "Work", "Personal"])
        self.category_selector.currentTextChanged.connect(self.filter_tasks)
        self.layout.addWidget(self.category_selector)

        # Task List
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        # Buttons
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Task")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.add_button.clicked.connect(self.add_task)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px;")
        self.delete_button.clicked.connect(self.delete_task)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        self.layout.addLayout(button_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Load tasks from file
        self.load_tasks()

    def add_task(self):
        task, ok = QInputDialog.getText(self, "Add Task", "Enter Task:")
        if ok and task:
            category, ok_category = QInputDialog.getItem(self, "Select Category", "Choose Category:", ["Work", "Personal"], editable=False)
            if ok_category:
                item = QListWidgetItem(f"[{category}] {task}")
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.task_list.addItem(item)
                self.save_tasks()

    def delete_task(self):
        selected_item = self.task_list.currentRow()
        if selected_item >= 0:
            self.task_list.takeItem(selected_item)
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Warning", "No task selected.")

    def filter_tasks(self):
        selected_category = self.category_selector.currentText()
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            item.setHidden(False if selected_category == "All" or f"[{selected_category}]" in item.text() else True)

    def save_tasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            tasks.append({"text": item.text(), "checked": item.checkState() == Qt.Checked})
        with open("tasks.json", "w") as file:
            json.dump(tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                for task in tasks:
                    item = QListWidgetItem(task["text"])
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Checked if task["checked"] else Qt.Unchecked)
                    self.task_list.addItem(item)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-family: Arial; font-size: 14px; }")
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())

