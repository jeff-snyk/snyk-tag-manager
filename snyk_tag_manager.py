import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QTreeView, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QModelIndex, Qt
import requests
import json

class ButtonStandardItem(QStandardItem):
    def __init__(self, button: QPushButton):
        super().__init__()
        self.button = button

class SnykTagManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_page = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Snyk Tag Manager")

        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create input layout
        input_layout = QGridLayout()
        main_layout.addLayout(input_layout)

        # API key input
        api_key_label = QLabel("Snyk API Token:")
        input_layout.addWidget(api_key_label, 0, 0)
        self.api_key_entry = QLineEdit()
        self.api_key_entry.setFixedWidth(300)
        input_layout.addWidget(self.api_key_entry, 0, 1)

        # Group ID input
        group_id_label = QLabel("Group ID:")
        input_layout.addWidget(group_id_label, 1, 0)
        self.group_id_entry = QLineEdit()
        self.group_id_entry.setFixedWidth(300)
        input_layout.addWidget(self.group_id_entry, 1, 1)
 
        # List tags button
        list_tags_button = QPushButton("List Tags")
        list_tags_button.clicked.connect(self.list_tags)
        main_layout.addWidget(list_tags_button)

        # Treeview
        self.tags_treeview = QTreeView()
        self.tags_treeview.setHeaderHidden(False)
        self.tags_treeview.setFixedHeight(500)
        main_layout.addWidget(self.tags_treeview)

        self.model = QStandardItemModel(0, 2)
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "Tag")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Delete")
        self.tags_treeview.setModel(self.model)
        self.tags_treeview.setColumnWidth(0, 300)
        self.tags_treeview.setColumnWidth(1, 75)

        # Navigation buttons
        nav_layout = QGridLayout()
        main_layout.addLayout(nav_layout)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        nav_layout.addWidget(self.back_button, 0, 0)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.go_next)
        self.next_button.setEnabled(False)
        nav_layout.addWidget(self.next_button, 0, 1)

        # Quit button
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)
        main_layout.addWidget(quit_button)

    def fetch_tags(self, api_key, group_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {api_key}"
        }
        url = f"https://api.snyk.io/v1/group/{group_id}/tags"
        response = requests.get(url, headers=headers)
        return response.json()

    def list_tags(self, page=0):
        api_key = self.api_key_entry.text()
        group_id = self.group_id_entry.text()

        if not api_key or not group_id:
            QMessageBox.critical(self, "Error", "Please provide both API token and Group ID.")
            return

        tag_data = self.fetch_tags(api_key, group_id)

        self.model.removeRows(0, self.model.rowCount())  # Clear the treeview before displaying new tags
        start_index = page * 25
        end_index = start_index + 25
        for tag in tag_data['tags'][start_index:end_index]:
            tag_item = QStandardItem(f"{tag['key']}: {tag['value']}")

            delete_button = QPushButton("Delete")
            # This makes them square grey buttons
            #delete_button.setStyleSheet("background-color: #D3D3D3;")
            delete_button.clicked.connect(lambda checked, r=self.model.rowCount(), t=tag: self.on_delete_button_click(r, t))
            delete_item = ButtonStandardItem(delete_button)

            self.model.appendRow([tag_item, delete_item])
            self.tags_treeview.setIndexWidget(delete_item.index(), delete_button)

        # Update navigation buttons state
        self.back_button.setEnabled(page > 0)
        self.next_button.setEnabled(end_index < len(tag_data['tags']))

    def on_delete_button_click(self, row, tag):
        tag_key, tag_value = tag['key'], tag['value']

        api_key = self.api_key_entry.text()
        group_id = self.group_id_entry.text()
        response_status, response_json = self.delete_tag(api_key, group_id, tag_key, tag_value)

        if response_status == 200:
            self.model.removeRow(row)
        else:
            if response_status == 403:
                message = f"Error deleting tag:\n\n{response_json['message']}. \n\nThis likely means there are projects using this tag."
            else:
                message = f"Failed to delete tag. Error code: {response_status}"
            QMessageBox.critical(self, "Error", message)

    def delete_tag(self, api_key, group_id, tag_key, tag_value):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {api_key}"
        }
        url = f"https://api.snyk.io/v1/group/{group_id}/tags/delete"
        payload = {
            "key": tag_key,
            "value": tag_value,
            "force": False
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code, response.json()

    def on_treeview_click(self, index: QModelIndex):
        row = index.row()
        column = index.column()

        if column == 1:
            tag = self.model.item(row, 0).text()
            tag_key, tag_value = tag.split(": ")

            api_key = self.api_key_entry.text()
            group_id = self.group_id_entry.text()
            response_status, response_json = self.delete_tag(api_key, group_id, tag_key, tag_value)

            if response_status == 200:
                self.model.removeRow(row)
            else:
                if response_status == 403:
                    message = f"Error deleting tag:\n\n{response_json['message']}. \n\nThis likely means there are projects using this tag."
                else:
                    message = f"Failed to delete tag. Error code: {response_status}"
                QMessageBox.critical(self, "Error", message)

    def go_back(self):
        self.current_page -= 1
        self.list_tags(self.current_page)

    def go_next(self):
        self.current_page += 1
        self.list_tags(self.current_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    snyk_tag_manager = SnykTagManager()
    snyk_tag_manager.show()
    sys.exit(app.exec())
