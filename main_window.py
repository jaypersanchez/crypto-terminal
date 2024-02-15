import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDesktopWidget, QStackedWidget
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QMovie, QScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EthSight Analytics")

        # Initialize the spinner
        self.initSpinner()
        
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
        
        # Adjust the window size to 50% of the screen size
        self.adjust_window_size(percentage=50)

    def adjust_window_size(self, percentage=50):
        screen = QApplication.primaryScreen().geometry()
        width = screen.width() * percentage / 100
        height = screen.height() * percentage / 100
        self.setGeometry(0, 0, int(width), int(height))
        self.center()

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initSpinner(self):
        # Spinner Label
        self.spinnerLabel = QLabel(self)
        self.spinnerMovie = QMovie("./assets/spinner.gif")
        self.spinnerLabel.setMovie(self.spinnerMovie)
        self.spinnerLabel.hide()  # Initially hide the spinner
        
         # Adjust window size first to ensure correct spinner positioning
        self.adjust_window_size(percentage=50)
        
        # Explicitly set the geometry of the spinnerLabel.  
        # This assumes your main window has a reasonable size, adjust as necessary
        screenWidth = self.frameGeometry().width()
        screenHeight = self.frameGeometry().height()
        spinnerWidth = 100  # Adjust as needed
        spinnerHeight = 100  # Adjust as needed
        # Calculate positions as integers
        x_position = int((screenWidth - spinnerWidth) / 2)
        y_position = int((screenHeight - spinnerHeight) / 2)

        # Now pass integers to setGeometry
        self.spinnerLabel.setGeometry(x_position, y_position, spinnerWidth, spinnerHeight)
    
    def showSpinner(self):
        self.spinnerLabel.show()
        self.spinnerMovie.start()

    def hideSpinner(self):
        self.spinnerLabel.hide()
        self.spinnerMovie.stop()

    def run_eth_previous_day_sentiment(self):
        self.showSpinner()
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

    def onScriptFinished(self):
        self.hideSpinner()
        # Handle script finished logic here
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
