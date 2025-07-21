import logging
import time

logger = logging.getLogger(__name__)


import logging
import threading
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from src.core.indexer import run_indexing
from src.core.vector.chunker import chunk_and_load_single_file
from src.core.vector.delete import delete_from_vectorstore_by_path

logger = logging.getLogger(__name__)


class ChangeHandler(FileSystemEventHandler):
    """A sophisticated file event handler that debounces events to prevent redundant indexing."""

    def __init__(self, watch_path: str | Path, debounce_interval: int = 2):
        super().__init__()
        self.watch_path = Path(watch_path)
        self.debounce_interval = debounce_interval
        self.timer: threading.Timer | None = None
        self.event_queue: list[FileSystemEvent] = []

    def _process_events(self):
        """Processes all events in the queue."""
        if not self.event_queue:
            return

        logger.info(f"Processing {len(self.event_queue)} events...")

        creations = set()
        deletions = set()
        modifications = set()

        for event in self.event_queue:
            if event.is_directory or event.src_path.endswith("~"):
                continue

            src_path = Path(event.src_path)

            if event.event_type == "created":
                creations.add(str(src_path))
            elif event.event_type == "deleted":
                deletions.add(str(src_path))
            elif event.event_type == "modified":
                modifications.add(str(src_path))
            elif event.event_type == "moved":
                deletions.add(str(src_path))

        self.event_queue.clear()

        for path in deletions:
            delete_from_vectorstore_by_path(path)

        for path in creations.union(modifications):
            delete_from_vectorstore_by_path(path)
            chunk_and_load_single_file(path)

        if deletions or creations or modifications:
            run_indexing(str(self.watch_path))

        logger.info("File change processing finished.")

    def _debounce_event(self, event: FileSystemEvent):
        """Cancels any pending processing and starts a new timer."""
        self.event_queue.append(event)

        if self.timer:
            self.timer.cancel()

        self.timer = threading.Timer(self.debounce_interval, self._process_events)
        self.timer.start()
        logger.info(f"Debouncing... next processing in {self.debounce_interval} seconds.")

    def on_modified(self, event: FileSystemEvent):
        if not event.is_directory:
            logger.info(f"[Watcher] File modified: {event.src_path}")
            self._debounce_event(event)

    def on_created(self, event: FileSystemEvent):
        logger.info(f"[Watcher] Created: {'Dir' if event.is_directory else 'File'}: {event.src_path}")
        self._debounce_event(event)

    def on_deleted(self, event: FileSystemEvent):
        logger.info(f"[Watcher] Deleted: {'Dir' if event.is_directory else 'File'}: {event.src_path}")
        self._debounce_event(event)

    def on_moved(self, event: FileSystemEvent):
        logger.info(f"[Watcher] Moved/Renamed: from {event.src_path} to {event.dest_path}")
        self._debounce_event(event)



def start_watcher(path: str | Path):
    """Starts the file system watcher."""
    logging.basicConfig(level=logging.INFO)
    logger.info(f"[Watcher] Initializing watcher for path: {path}")

    watch_path = Path(path).resolve()
    if not watch_path.is_dir():
        logger.error(f"[Watcher] Path is not a directory: {watch_path}")
        return

    logger.info(f"[Watcher] Starting observer on absolute path: {watch_path}")

    observer = Observer()
    observer.schedule(ChangeHandler(watch_path=watch_path), str(watch_path), recursive=True)
    observer.start()

    logger.info("[Watcher] Observer started successfully. Waiting for file changes.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("[Watcher] Keyboard interrupt received, stopping observer.")
    finally:
        observer.stop()
        observer.join()
        logger.info("[Watcher] Observer stopped.")
