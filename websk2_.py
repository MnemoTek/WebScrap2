import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QLabel,
    QTableWidget, QTableWidgetItem,
    QFileDialog
)

class ScraperApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Scraper Tool")
        self.setGeometry(200,200,700,500)

        layout = QVBoxLayout()

        self.label = QLabel("Enter URL")
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        self.url_input.setText("https://books.toscrape.com/")
        layout.addWidget(self.url_input)

        self.scrape_button = QPushButton("Scrape Data")
        self.scrape_button.clicked.connect(self.scrape_data)
        layout.addWidget(self.scrape_button)

        self.export_button = QPushButton("Export CSV")
        self.export_button.clicked.connect(self.export_csv)
        layout.addWidget(self.export_button)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.data = []

    def scrape_data(self):

        url = self.url_input.text()

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        books = []

        for book in soup.find_all("article", class_="product_pod"):

            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text

            books.append([title, price])

        self.data = books

        self.table.setRowCount(len(books))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Title", "Price"])

        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(value))

    def export_csv(self):

        if not self.data:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            "",
            "CSV Files (*.csv)"
        )

        if path:
            df = pd.DataFrame(self.data, columns=["Title","Price"])
            df.to_csv(path, index=False)


app = QApplication(sys.argv)

window = ScraperApp()
window.show()

sys.exit(app.exec())
