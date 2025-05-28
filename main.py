import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
class WeatherAPP(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Podaj nazwę miasta", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Podaj", self)
        self.temperature_label = QLabel("34°C", self)
        self.emoji_label= QLabel("☀️",self)
        self.description_label = QLabel("jest pogodnie", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Aplikacja Pogodowa")


        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
        Qlabel, QPushButton{
            font-family: Times New Roman;
            font-size: 24px;
        }
        QLabel#city_label{
            font-size: 24px;
            font-style: italic;
        }
        QLineEdit#city_input{
            font-size: 24px;
        }
        QPushButton#get_weather_button{
            font-size: 24px;
            font-weight: bold;
        }
        QLabel#temperature_label{
            font-size: 28px;
        }
        QLabel#emoji_label{
            font-size: 100px;
            font-family: Segoe UI emoji;
        }
        QLabel#description_label{
            font-size: 50px;
        }
        
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherAPP()
    weather_app.show()
    sys.exit(app.exec_())