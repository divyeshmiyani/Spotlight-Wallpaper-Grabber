import os
import shutil
import PIL.Image


# fetch Wallpaper/s
class Base:
    def __init__(self):
        # Resolution of Wallpaper
        self.x = 1900
        self.y = 1000
        self.temp = os.path.dirname(os.path.abspath(__file__))  # returns path of this file

        source = os.path.expanduser(
            "~") + r"/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets"
        self.temp = os.path.join(self.temp, 'temp')

        # copies files
        shutil.copytree(source, self.temp)

        # rename files
        os.chdir(self.temp)
        file_list = os.listdir()
        for f in file_list:
            os.rename(f, f + '.jpg')

        # wallpaper array
        file_list = os.listdir()
        self.array = []
        for f in file_list:
            temp1 = os.path.join(self.temp, f)
            img = PIL.Image.open(temp1)
            wid, hgt = img.size
            img.close()
            if wid > self.x and hgt > self.y:
                self.array.append(f)

    def __del__(self):
        # delete temp folder
        os.chdir('..')
        shutil.rmtree(self.temp)


# Saves Wallpaper/s to local
class SaveToLocal(Base):
    def __init__(self):
        super().__init__()

    def execute(self, path):
        temp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        filtered = list(filter(lambda x: not os.path.exists(os.path.join(path, x)), self.array))
        for f in filtered:
            if not os.path.exists(os.path.join(path, f)):
                shutil.move(os.path.join(temp, f), path)
        return len(filtered)
