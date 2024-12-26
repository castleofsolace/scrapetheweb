import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QStatusBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class WebScraper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScrapeTheWeb")
        self.setWindowIcon(QIcon('scraper.ico'))
        self.resize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #222222;
                color: #FFFFFF;
            }
            QWidget {
                background-color: #222222;
                color: #FFFFFF;
            }
            QLineEdit, QTextEdit {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #444444;
                color: #FFFFFF;
                border: 1px solid #666666;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
            QLabel {
                color: #AAAAAA;
                font-size: 12px;
            }
            QStatusBar {
                background-color: #111111;
                color: #AAAAAA;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.url_label = QLabel("Enter URL:")
        self.layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.example.com")
        self.layout.addWidget(self.url_input)

        self.scrape_button = QPushButton("Scrape Website")
        self.scrape_button.clicked.connect(self.scrape_website)
        self.scrape_button.setIcon(QIcon('scrape.png'))
        self.layout.addWidget(self.scrape_button)

        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_output)
        self.save_button.setIcon(QIcon('save.png'))
        self.save_button.setEnabled(False)
        self.layout.addWidget(self.save_button)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def scrape_website(self):
        url = self.url_input.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract all text from the webpage
            text = soup.get_text()
            output = text
            self.output_text.setPlainText(output)
            self.save_button.setEnabled(True)
            self.status_bar.showMessage("Scraping completed successfully.", 5000)
            print(output)  # Verify the output
        except requests.exceptions.HTTPError as http_err:
            self.status_bar.showMessage(f"HTTP error occurred: {http_err}", 5000)
        except Exception as err:
            self.status_bar.showMessage(f"An error occurred: {err}", 5000)

    def save_output(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Output", "",
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            text_to_save = self.output_text.toPlainText()
            if text_to_save:
                try:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(text_to_save)
                    self.status_bar.showMessage(f"Output saved to {file_name}", 5000)
                except Exception as e:
                    self.status_bar.showMessage(f"Error saving file: {e}", 5000)
            else:
                self.status_bar.showMessage("No data to save.", 5000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scraper = WebScraper()
    scraper.show()
    sys.exit(app.exec_())