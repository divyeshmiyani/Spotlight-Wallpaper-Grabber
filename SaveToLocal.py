import shutil
import os


# Saves Wallpaper/s to local
class SaveToLocal:
    def execute(self, path, folder):
        file_name = path.split('\\')[-1]
        if os.path.exists(folder + '/' + file_name + '.jpg'):
            return
        shutil.copy(path, folder)
        os.rename(folder + '/' + file_name, folder + '/' + file_name + '.jpg')
