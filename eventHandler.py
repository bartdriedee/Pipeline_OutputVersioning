import os, time, shutil, re
from watchdog.events import RegexMatchingEventHandler


class ImagesEventHandler(RegexMatchingEventHandler):
    # exclude files with "proxy" in their name from the inputs
    IMAGES_REGEX = [r"^((?!(edit|EDIT)).)*(v|V)\d+(.jpg)$"]

    def __init__(self):
        super(ImagesEventHandler,self).__init__(self.IMAGES_REGEX)
        self.last_file_processed = None

    # called when a file or a directory is created
    def on_created(self, event):
        if self.filterEvents(event):
            if self.writingFinished(event):
                self.process(event)

    # called when a file or directory is changed
    def on_moved(self, event):
        if self.filterEvents(event):
            if self.writingFinished(event):
                self.process(event)

    def writingFinished(self,event):
        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(1)
        file_done = False
        while not file_done:
            try:
                os.rename(event.src_path, event.src_path)
                file_done = True
            except:
                pass
        return True

    def filterEvents(self,event):
        if "04_OUTPUT" and "02_SHOTS" in event.src_path:
            self.last_file_processed = event.src_path
            return True


    def process(self, event):
        folder = os.path.dirname(event.src_path)
        filename, extension = os.path.splitext(os.path.basename(event.src_path))
        filename_copy = re.sub(r'(v|V)\d+', "EDIT", filename)
        copy_path = "{0}\\{1}{2}".format(folder, filename_copy, extension.lower())
        print("Updating {} with {}".format(copy_path, event.src_path))
        shutil.copyfile(event.src_path, copy_path, follow_symlinks=False)

