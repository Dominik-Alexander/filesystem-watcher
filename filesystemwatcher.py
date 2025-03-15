import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time

def main() -> None:
    
    """
    Monitors a directory for a file to be downloaded.

    Looks for path and file name as arguments.

    If the file is found, it stops the observer.

    If the program is stopped with Ctrl-C, it stops the observer.

    :return: None
    """
    try:
        expected_path_to_file = ''.join(sys.argv[1])
    except Exception:
        print("Invalid path.")
        return
    
    try:
        path_list = expected_path_to_file.split("/")
        file_name = path_list[-1]
        download_folder = "/".join(path_list[:-1])
    except Exception:
        print("Could not get path and file name from input.")
        return

    class DownloadHandler(FileSystemEventHandler):
        def __init__(self, file_name):
            self._file_name = file_name

        def on_created(self, event):
            if Path(event.src_path).name == self._file_name:
                print("File found!")
                observer.stop()

    event_handler = DownloadHandler(file_name)
    observer = Observer()
    observer.schedule(event_handler, download_folder, recursive=False)
    observer.start()

    print("Monitoring for file download...")

    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if '__name__' == '__main__':
    main()
