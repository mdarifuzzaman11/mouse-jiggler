import sys
import pyautogui
import time
import threading
import random
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

class ClickableLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl("https://github.com/mdarifuzzaman11/mouse-jiggler"))

class MouseJigglerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.jiggle_interval = 15  # default interval in seconds
        self.jiggling = False
        self.initUI()
        self.jiggle_thread = threading.Thread(target=self.jiggle_mouse, daemon=True)

    def initUI(self):
        self.setWindowTitle("Mouse Jiggler Settings")
        self.layout = QVBoxLayout()

        self.label = QLabel("Set Mouse Movement Interval (Seconds):")
        self.layout.addWidget(self.label)

        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(60)
        self.spinBox.setValue(15)
        self.spinBox.valueChanged.connect(self.checkInterval)
        self.layout.addWidget(self.spinBox)

        self.toggleButton = QPushButton("Start Jiggling")
        self.setStyleForToggleButton()
        self.toggleButton.clicked.connect(self.toggleJiggling)
        self.layout.addWidget(self.toggleButton, alignment=Qt.AlignCenter)

        # GitHub Link and Version Info
        hbox = QHBoxLayout()
        githubPixmap = QPixmap('github_icon.png')  # Replace with your GitHub icon path
        self.githubIcon = ClickableLabel(githubPixmap.scaled(40, 40, Qt.KeepAspectRatio))
        hbox.addWidget(self.githubIcon)
        versionLabel = QLabel("Version 1.0 - Last Modified 12/28/2023\nOpen Source Project by MD Arifuzzaman")
        hbox.addWidget(versionLabel)
        self.layout.addLayout(hbox)

        self.setLayout(self.layout)

    def checkInterval(self):
        if self.spinBox.value() < 10:
            QMessageBox.warning(self, "Interval Too Short", "This interval can be annoying and difficult to stop. Please select a time of 10 seconds or higher.")
            self.spinBox.setValue(10)

    def setStyleForToggleButton(self):
        color = "green" if not self.jiggling else "red"
        self.toggleButton.setText("Start Jiggling" if not self.jiggling else "Stop Jiggling")
        self.toggleButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 20px; 
                padding: 10px;
            }}
            QPushButton:pressed {{
                background-color: {'#006400' if color == 'green' else '#8B0000'};
            }}
        """)
        self.toggleButton.setFixedWidth(120)
        self.toggleButton.setFixedHeight(40)

    def jiggle_mouse(self):
        while self.jiggling:
            self.realistic_movement()
            time.sleep(self.jiggle_interval)

    def realistic_movement(self):
        for _ in range(4):
            pyautogui.moveRel(random.randint(5, 10), random.randint(5, 10), duration=0.2)
            pyautogui.moveRel(random.randint(-10, -5), random.randint(-10, -5), duration=0.2)

    def toggleJiggling(self):
        self.jiggling = not self.jiggling
        if self.jiggling:
            self.jiggle_thread = threading.Thread(target=self.jiggle_mouse, daemon=True)
            self.jiggle_thread.start()
        self.setStyleForToggleButton()

def main():
    app = QApplication(sys.argv)

    mainWidget = MouseJigglerApp()
    mainWidget.show()

    trayIcon = QSystemTrayIcon(QIcon("icon.png"), app)
    menu = QMenu()

    exitAction = QAction("Exit", trayIcon)
    exitAction.triggered.connect(app.quit)
    menu.addAction(exitAction)

    settingsAction = QAction("Settings", trayIcon)
    settingsAction.triggered.connect(mainWidget.show)
    menu.addAction(settingsAction)

    trayIcon.setContextMenu(menu)
    trayIcon.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
