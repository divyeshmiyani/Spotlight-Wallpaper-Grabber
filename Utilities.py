import os
from SaveToGoogleDrive import SaveToGoogleDrive
from SaveToLocal import SaveToLocal
import PIL.Image as Img

source = os.path.expanduser("~") + r"\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy" \
                                   r"\LocalState\Assets"


class File:
    def __init__(self):
        self.path = ''
        self.dest = ''
        self.folder = ''
        self.x = 1900
        self.y = 1000

    def save_all(self, location: str, dest: str):
        self.folder = location
        self.dest = dest
        file_list = [os.path.join(source, i) for i in os.listdir(source)]
        for path in file_list:
            self.perform(path)

    def is_valid(self):
        img = Img.open(self.path)
        wid, hgt = img.size
        return wid > self.x and hgt > self.y

    def perform(self, path):
        self.path = path
        if self.is_valid():
            self.save()

    def save(self):
        if self.dest == 'local':
            SaveToLocal().execute(self.path, self.folder)
        elif self.dest == 'Googledrive':
            SaveToGoogleDrive().execute(self.path)
