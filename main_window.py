import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EthSight Analytics")

        # Layout
        layout = QVBoxLayout()

        # Labels
        self.label = QLabel("Select an action:")
        layout.addWidget(self.label)

        # Buttons for running scripts
        self.ethButton = QPushButton("Run ETH Monthly Price Action")
        self.ethButton.clicked.connect(self.run_eth_script)
        layout.addWidget(self.ethButton)
        
        # Buttons for running scripts
        self.ethButton = QPushButton("Run ETH Previous Day Sentiment")
        self.ethButton.clicked.connect(self.run_eth_previous_day_sentiment)
        layout.addWidget(self.ethButton)

        self.solButton = QPushButton("Run SOL Monthly Price Action")
        self.solButton.clicked.connect(self.run_sol_script)
        layout.addWidget(self.solButton)
        
        # Buttons for running scripts
        self.solButton = QPushButton("Run SOL Previous Day Sentiment")
        self.solButton.clicked.connect(self.run_sol_previous_day_sentiment)
        layout.addWidget(self.solButton)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_eth_previous_day_sentiment(self):
        self.process = QProcess(self)
        self.process.finished.connect(self.script_finished)
        # Assuming eth_monthly_price_action.py is in the root directory
        self.process.start("python", ["eth_previous_day_sentiment.py"])

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
    
    def run_sol_previous_day_sentiment(self):
        self.process = QProcess(self)
        self.process.finished.connect(self.script_finished)
        # Assuming sol_monthly_price_action.py is in the root directory
        self.process.start("python", ["sol_previous_day_sentiment.py"])

    def script_finished(self):
        self.label.setText("Script execution finished!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
