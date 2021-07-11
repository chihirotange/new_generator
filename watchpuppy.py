import watchdog.events
import watchdog.observers
import time
import os
from shutil import move
from PIL import Image

img_size = (2000,2257)

def pngWatchDog():
    workingDir = r"D:\monitor" # dan toi folder lam viec
    # targetDir = r"D:\Chii chan drive\shibe NFT\hires_assets\bg" # dan toi folder assets
    targetDir = r"D:\Chii chan drive\shibe NFT\hires_assets\fixed_assets" # dan toi folder assets
    bodyTypes = ["normal", "android", "anatomicanis"]
    assetsDir = os.listdir(targetDir)

    def doMystuff(dapath):
        # when magic happens :v
        fileName = os.path.basename(dapath)
        fileNameWoExt = os.path.splitext(fileName)[0]
        nameCues = fileNameWoExt.split("_")
        if nameCues[0] == 'bg':
            correctCue = 'bg'
        elif nameCues[0] == 'solid':
            correctCue = 'solid'
        elif len(nameCues) == 5 and nameCues[1] == 'eye':
            correctCue = 'eye'
        elif nameCues[0] in bodyTypes and len(nameCues) == 3:
            correctCue = "_".join(['body', nameCues[-1]])
        else:
            correctCue = "_".join([nameCues[0], nameCues[-1]])

        for _ in range(len(assetsDir)):
            if correctCue in assetsDir[_]:
                path_moved = os.path.join(targetDir, assetsDir[_], fileName)
                print(path_moved)
                img = Image.open(dapath)
                img_rz = img.resize(img_size)
                img_rz.save(dapath)
                move(dapath, path_moved)

    class Handler(watchdog.events.PatternMatchingEventHandler):

        def __init__(self):
            # Set the patterns for PatternMatchingEventHandler
            watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.png'],
                                                                   ignore_directories=True, case_sensitive=False)
        def on_created(self, event):
            print("Created " + event.src_path)
            # print("Watchdog received created event - % s." % event.src_path)
            init_size = -1
            while True:
                current_size = os.path.getsize(event.src_path)
                if current_size == init_size:
                    break
                else:
                    init_size = os.path.getsize(event.src_path)
                    time.sleep(0.5)
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