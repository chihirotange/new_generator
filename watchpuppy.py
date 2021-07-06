import watchdog.events
import watchdog.observers
import time
import os
from shutil import move
from PIL import Image

img_size = (2000,2257)

def pngWatchDog():
    workingDir = r"E:\chiichan\monitor" # dan toi folder lam viec
    targetDir = r"E:\chiichan\my drive\shibe NFT\hires_assets\fixed_assets" # dan toi folder assets
    bodyTypes = ["normal", "android", "anatomicanis"]
    assetsDir = os.listdir(targetDir)

    def doMystuff(dapath):
        # when magic happens :v
        fileName = os.path.basename(dapath)
        fileNameWoExt = os.path.splitext(fileName)[0]
        nameCues = fileNameWoExt.split("_")
        if nameCues[0] in bodyTypes:
            correctCue = "_".join([nameCues[1], nameCues[-1]])
        else:
            correctCue = "_".join([nameCues[0], nameCues[-1]])

        for _ in range(len(assetsDir)):
            if correctCue in assetsDir[_]:
                path_moved = os.path.join(targetDir, assetsDir[_], fileName)
                img = Image.open(dapath)
                img_rz = img.resize(img_size)
                img_rz.save(dapath)
                move(dapath, path_moved)

        return path_moved
    class Handler(watchdog.events.PatternMatchingEventHandler):

        def __init__(self):
            # Set the patterns for PatternMatchingEventHandler
            watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.png'],
                                                                   ignore_directories=True, case_sensitive=False)
        def on_created(self, event):
            print("Created " + event.src_path)
            # print("Watchdog received created event - % s." % event.src_path)
            print(f'Moved {doMystuff(event.src_path)}')

        # def on_modified(self, event):
        #     print("Modified " + event.src_path)
            # print("Watchdog received modified event - % s." % event.src_path)
            # doMystuff(event.src_path)

    if __name__ == "__main__":
        src_path = workingDir
        event_handler = Handler()
        observer = watchdog.observers.Observer()
        observer.schedule(event_handler, path=src_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

pngWatchDog()