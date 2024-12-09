# App Design

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView

from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expenses, delete_expenses



class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()
        


    def settings(self):
        self.setGeometry(750, 300, 550, 500)  #width and height of application
        self.setWindowTitle("Expense Traker App")


    # Design
    def initUI(self):
        # Create all Objects
        self.date_box =QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        self.btn_delete = QPushButton("Delete Expense")

        self.btn_add.setObjectName("addButton")
        self.btn_delete.setObjectName("deleteButton")

        
        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)

        # Add Widgets to a Layout (Row/Column)
        self.setup_layout()

        self.apply_styles()

    def  setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        # Row 1
        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        # Row 2

        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)

    
    def apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #e3e9f2;
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
        }

        QLabel {
            font-size: 16px;
            color: #2c3e50;
            font-weight: bold;
            padding: 5px;
        }

        QLineEdit, QComboBox, QDateEdit {
            background-color: #fff;
            font-size: 14px;
            color: #333;
            border: 1px solid #b0bfc6;
            border-radius: 5px;
            padding: 5px;
        }

        QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
            border: 1px solid #4caf50;
        }
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 1px solid #2a9d8f;
            background-color: #f5f9fc;
        }

        QTableWidget {
            background-color: #fff;
            alternate-background-color: #f2f7fb;
            gridline-color: #c0c9d0;
            selection-background-color: #4caf50;
            selection-color: white;
            font-size: 14px;
            border: 1px solid #cfd9e1;
        }

        QHeaderView::section {
            background-color: #4caf50;
            color: white;
            font-weight: bold;
            padding: 4px;
            border: 1px solid #cfd9e1;
        }

        QScrollBar:vertical {
            width: 12px;
            background-color: #f0f0f0;
            border: none;
        }
        QScrollBar::handle:vertical {
            background-color: #4caf50;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }

        QPushButton {
            background-color: #4caf50;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QPushButton:disabled {
            background-color: #c8c8c8;
            color: #6e6e6e;
        }

        QPushButton#addButton {
            background-color: #4caf50;
        }
        QPushButton#addButton:hover {
            background-color: #45a049;
        }
        QPushButton#addButton:pressed {
            background-color: #3d8b40;
        }

        QPushButton#deleteButton {
            background-color: #e74c3c;
            color: white;
        }
        QPushButton#deleteButton:hover {
            background-color: #c0392b;
        }
        QPushButton#deleteButton:pressed {
            background-color: #a93226;
        }

        QToolTip {
            background-color: #2c3e50;
            color: #ffffff;
            border: 1px solid #333;
            font-size: 12px;
            padding: 5px;
            border-radius: 4px;
        }
        """)



    def populate_dropdown(self):
        categories = ["Food","Rent","Bills","Entertainment","Shopping","Other"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText() #QComboBox 
        amount = self.amount.text() #QLineEdit
        description = self.description.text()


        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description can not be empty")
            return
        
        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
            #Clear Inputs
        else:
            QMessageBox.critical(self, "Error","Failed to add expense")


    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "uh oh", "You need to choose a row to delete.")
            return
        
        expense_id = int(self.table.item(selected_row, 0).text())
        # Correct the QMessageBox.StandardButton reference
        confirm = QMessageBox.question(
            self,
            "Confirm",
            "Are you sure you want to delete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()

