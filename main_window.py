import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDesktopWidget
from PyQt5.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EthSight Analytics")

        # Adjust the window size to 50% of the screen size
        self.adjust_window_size(percentage=50)

        # Layout
        layout = QVBoxLayout()

        # Labels
        self.label = QLabel("Select an action:")
        layout.addWidget(self.label)

        # Buttons for running scripts
        self.ethButton = QPushButton("Run ETH Monthly Price Action")
        self.ethButton.clicked.connect(self.run_eth_script)
        layout.addWidget(self.ethButton)

        self.solButton = QPushButton("Run SOL Monthly Price Action")
        self.solButton.clicked.connect(self.run_sol_script)
        layout.addWidget(self.solButton)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def adjust_window_size(self, percentage=50):
        screen = QDesktopWidget().screenGeometry()
        # Calculate width and height based on the percentage of the screen size
        width = int(screen.width() * percentage / 100)  # Convert to int
        height = int(screen.height() * percentage / 100)  # Convert to int
        self.setGeometry(0, 0, width, height)
        self.center()


    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run_eth_script(self):
        self.process = QProcess(self)
        self.process.finished.connect(self.script_finished)
        # Assuming eth_monthly_price_action.py is in the root directory
        self.process.start("python", ["eth_monthly_price_action.py", "2022-09-01", "2022-09-30"])

    def run_sol_script(self):
        self.process = QProcess(self)
        self.process.finished.connect(self.script_finished)
        # Assuming sol_monthly_price_action.py is in the root directory
        self.process.start("python", ["sol_monthly_price_action.py", "2022-09-01", "2022-09-30"])

    def script_finished(self):
        self.label.setText("Script execution finished!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
