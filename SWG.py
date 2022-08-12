from SaveToGoogleDrive import SaveToGoogleDrive
from datetime import datetime
from Utilities import File
import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import json
import os
from threading import Thread

data = {
    "syncTime": 'Not Yet',
    "filesUploaded": []
}

try:
    jsonfile = open("data.json")
    data = json.load(jsonfile)
except FileNotFoundError:
    with open('data.json', 'w') as fp:
        json.dump(data, fp)


class MainWindow(Qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.destination_path = ""

        # Add a title
        self.setWindowTitle("Spotlight Wallpaper Grabber")
        layout = Qtw.QFormLayout()
        self.setLayout(layout)
        self.setFont(Qtg.QFont("San Francisco", 10))

        label = Qtw.QLabel("Save Wallpaper To ")
        label.setFont(Qtg.QFont("San Francisco", 18))

        # Path Entry Box
        self.pathLabel = Qtw.QLineEdit(self)

        # Browse Button
        browseButton = Qtw.QPushButton("Browse")
        browseButton.clicked.connect(lambda: self.browse())

        # Save Button
        self.saveButton = Qtw.QPushButton("Save")
        self.saveButton.clicked.connect(lambda: Thread(target=self.execute).start())

        # GDrive Connect Button
        self.connectButton = Qtw.QPushButton("Connect")
        self.connectButton.clicked.connect(lambda: Thread(target=self.connectToGDrive).start())
        self.connectButton.setEnabled(False)

        # GDrive Sync Button
        self.syncButton = Qtw.QPushButton("Sync")
        self.syncButton.clicked.connect(lambda: Thread(target=self.sync).start())
        self.syncButton.setEnabled(False)

        if os.path.exists('credentials.json'):
            self.connectButton.setEnabled(True)
            if os.path.exists('token.json'):
                self.syncButton.setEnabled(True)

        # Last Synced
        lastSyncedLabel = Qtw.QLabel("Last Synced")
        self.lastSyncedTimeLabel = Qtw.QLabel(data['syncTime'])

        # Close Button
        closeButton = Qtw.QPushButton("Close")
        closeButton.clicked.connect(lambda: self.Close_all())

        # Label HBox
        HBox0 = Qtw.QHBoxLayout()
        HBox0.addWidget(label)

        # First HBox
        HBox1 = Qtw.QHBoxLayout()
        HBox1.addWidget(self.pathLabel)
        HBox1.addWidget(browseButton)
        HBox1.addWidget(self.saveButton)

        # Second HBox
        HBox2 = Qtw.QHBoxLayout()
        HBox2.addWidget(self.connectButton)
        HBox2.addWidget(self.syncButton)

        # Third HBox
        HBox3 = Qtw.QHBoxLayout()
        HBox3.addWidget(lastSyncedLabel)
        HBox3.addWidget(self.lastSyncedTimeLabel)
        HBox3.setAlignment(Qtc.Qt.AlignCenter)

        # Bottom HBox
        HBottom = Qtw.QHBoxLayout()
        HBottom.addWidget(closeButton)
        HBottom.setAlignment(Qtc.Qt.AlignRight)

        # Main Window Layout
        layout.addRow(HBox0)
        layout.addRow("Local Directory Path", HBox1)
        layout.addRow("Google Drive", HBox2)
        layout.addRow(HBox3)
        layout.addRow(HBottom)
        self.show()

    def browse(self):
        self.destination_path = Qtw.QFileDialog.getExistingDirectory()
        self.pathLabel.setText(self.destination_path)

    def connectToGDrive(self):
        self.connectButton.setEnabled(False)
        SaveToGoogleDrive()
        self.connectButton.setEnabled(True)

        if os.path.exists('token.json'):
            self.syncButton.setEnabled(True)

    def sync(self):
        self.syncButton.setEnabled(False)
        File().save_all(location='', dest='Googledrive')
        self.syncButton.setEnabled(True)

        with open("data.json") as jsonfile:
            data = json.load(jsonfile)

        data['syncTime'] = datetime.now().strftime("on %b %d %Y at %I:%M %p")
        self.lastSyncedTimeLabel.setText(data['syncTime'])

        with open('data.json', 'w') as fp:
            json.dump(data, fp)

    def Close_all(self):
        self.close()

    def execute(self):
        self.saveButton.setEnabled(False)
        if not self.destination_path:
            self.browse()
        if self.destination_path:
            File().save_all(location=self.destination_path, dest='local')
        self.saveButton.setEnabled(True)


app = Qtw.QApplication([])
mw = MainWindow()

app.exec_()
