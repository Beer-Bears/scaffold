import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from src.core.indexer import run_indexing


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, debounce_interval=15):
        self.debounce_interval = debounce_interval
        self.timer = None

    def on_any_event(self, event: FileSystemEvent):
        if event.is_directory:
            return

        if self.timer:
            self.timer.cancel()

        self.timer = threading.Timer(self.debounce_interval, run_indexing, [event])
        self.timer.start()


def start_watcher(path: str | Path):
    observer = Observer()
    observer.schedule(ChangeHandler(), path, recursive=True)
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
