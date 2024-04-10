import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, QStatusBar, QMessageBox, QFileDialog)
from symtab import SymbolTable

class SymbolTableGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_symbol_table = SymbolTable()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Symbol Table Manager')
        self.setGeometry(100, 100, 600, 600)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Ready')

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Identifier", "Kind", "Type"])

        self.identifier_input = QLineEdit()
        self.identifier_input.setPlaceholderText("Identifier")
        self.kind_input = QLineEdit()
        self.kind_input.setPlaceholderText("Kind")
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Type")

        layout = QVBoxLayout()
        layout.addWidget(self.identifier_input)
        layout.addWidget(self.kind_input)
        layout.addWidget(self.type_input)

        buttons = {
            "Enter Scope": self.enter_scope,
            "Exit Scope": self.exit_scope,
            "Insert Symbol": self.insert_symbol,
            "Lookup Symbol": self.lookup_symbol,
            "Delete Symbol": self.delete_symbol,
            "Save Table": self.save_table,
            "Load Table": self.load_table,
            "Clear Table": self.clear_table
        }

        for text, func in buttons.items():
            button = QPushButton(text, self)
            button.clicked.connect(func)
            layout.addWidget(button)

        layout.addWidget(self.tableWidget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QPushButton {
                background-color: #A3C1DA; padding: 8px;
                border-radius: 5px; margin: 2px;
            }
            QPushButton:hover {
                background-color: #779ECB;
            }
            QLineEdit {
                padding: 8px; margin: 2px;
                border-radius: 5px;
                border: 1px solid #A3C1DA;
            }
            QLabel {
                font-weight: bold; margin: 2px;
            }
            QTableWidget {
                gridline-color: #A3C1DA;
                border-radius: 5px; padding: 8px;
                selection-background-color: #D3E0EA;
            }
            QStatusBar {
                font-weight: bold;
            }
        """)

    def enter_scope(self):
        self.current_symbol_table = self.current_symbol_table.enter_scope()
        self.update_scope_indicator()
        self.refresh_table()

    def exit_scope(self):
        if self.current_symbol_table.parent:
            self.current_symbol_table = self.current_symbol_table.exit_scope()
            self.update_scope_indicator()
            self.refresh_table()
        else:
            self.statusBar.showMessage('No parent scope to exit to.')

    def insert_symbol(self):
        identifier = self.identifier_input.text().strip()
        kind = self.kind_input.text().strip()
        type_ = self.type_input.text().strip()
        if not identifier or not kind or not type_:
            QMessageBox.warning(self, 'Warning', 'All fields are required.')
            return

        if self.current_symbol_table.insert(identifier, kind, type_):
            self.statusBar.showMessage(f'Symbol {identifier} inserted successfully.')
            self.refresh_table()
        else:
            QMessageBox.warning(self, 'Warning', f'Symbol {identifier} already exists.')

    def lookup_symbol(self):
        identifier = self.identifier_input.text().strip()
        entry = self.current_symbol_table.lookup(identifier)
        if entry:
            self.statusBar.showMessage(f'Found: Identifier="{entry.identifier}", Kind="{entry.kind}", Type="{entry.type}"')
            self.highlight_symbol(identifier)
        else:
            QMessageBox.warning(self, 'Warning', f'Symbol "{identifier}" not found.')
            self.statusBar.clearMessage()

    def delete_symbol(self):
        identifier = self.identifier_input.text().strip()
        if self.current_symbol_table.delete(identifier):
            self.statusBar.showMessage(f'Symbol {identifier} deleted successfully.')
            self.refresh_table()
        else:
            QMessageBox.warning(self, 'Warning', f'Symbol "{identifier}" not found.')

    def save_table(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Symbol Table", "", "JSON Files (*.json)")
        if filePath:
            with open(filePath, 'w') as file:
                json.dump(self.current_symbol_table.serialize(), file)
            self.statusBar.showMessage('Symbol table saved successfully.')

    def load_table(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Symbol Table", "", "JSON Files (*.json)")
        if filePath:
            with open(filePath, 'r') as file:
                data = json.load(file)
            self.current_symbol_table = SymbolTable()
            self.current_symbol_table.deserialize(data)
            self.update_scope_indicator()
            self.refresh_table()
            self.statusBar.showMessage('Symbol table loaded successfully.')

    def clear_table(self):
        self.current_symbol_table = SymbolTable()
        self.update_scope_indicator()
        self.refresh_table()
        self.statusBar.showMessage('Symbol table cleared.')

    def refresh_table(self):
        self.tableWidget.setRowCount(0)
        for entry in self.current_symbol_table.entries:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(entry.identifier))
            self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(entry.kind))
            self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(entry.type))


    def update_scope_indicator(self):
        # Update the label that indicates the current scope level
        level = 0
        scope = self.current_symbol_table
        while scope.parent:
            level += 1
            scope = scope.parent
        self.statusBar.showMessage(f'Current Scope Level: {level}')

    def highlight_symbol(self, identifier):
        # Highlights the row in the table that corresponds to the identifier
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 0).text() == identifier:
                self.tableWidget.selectRow(i)
                return
        QMessageBox.information(self, 'Symbol Not Found', f'The symbol "{identifier}" was not found in the current scope.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SymbolTableGUI()
    ex.show()
    sys.exit(app.exec_())
