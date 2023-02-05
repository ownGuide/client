import os
import time

from watchdog.observers.polling import PollingObserver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from dirsync import sync

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        source_base_path = base_paths["yadisk"]
        destination_base_path = base_paths["local"]
        current_event_path = os.path.dirname(os.path.abspath(event.src_path))
        if current_event_path.startswith(base_paths["local"]):
            source_base_path, destination_base_path = destination_base_path, source_base_path
        relpath = os.path.relpath(current_event_path, source_base_path)
        source = os.path.join(source_base_path, relpath)
        destination = os.path.join(destination_base_path, relpath)
        time.sleep(5)
        sync(source, destination, "sync", purge=True)
               


def monitor_folders(yadisk_path, local_path):
    base_paths["yadisk"] = yadisk_path
    base_paths["local"] = local_path
    
    handler = Handler()
    
    watchers = []

    for key, value in base_paths.items():
        if key == "yadisk":
            watcher = PollingObserver()
        else:
            watcher = Observer()
        watcher.schedule(handler, base_paths[key], recursive=True)
        watcher.start()
        watchers.append(watcher)

    try:
       while True:
           time.sleep(5)
    except:
        for watcher in watchers:
            watcher.stop()
        print("Error")

    for watcher in watchers:
        watcher.join()


base_paths = {}
