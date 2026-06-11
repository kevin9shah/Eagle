import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.ingestion.vector_db import ingest_file

class IngestionHandler(FileSystemEventHandler):

    def on_created(self,event):
        if not event.is_directory and event.src_path.endswith('.pdf'):
            logging.info(f"New PDF Detected: {event.src_path}")
            ingest_file(event.src_path)
        
    def on_modified(self,event):
        if not event.is_directory and event.src_path.endswith('.pdf'):
            logging.info(f"Modified PDF Detected: {event.src_path}")
            ingest_file(event.src_path)
    
def watch():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    path = sys.argv[1] if len(sys.argv) > 1 else "/Users/kevinshah/Downloads"

    print(f"watching directory : {path}")

    print("Initial Scan: Walking directory...")
    import os
    for root,dirs,files in os.walk(path):
        for file_name in files:
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root,file_name)
                ingest_file(file_path)

    event_handler = IngestionHandler()
    observer = Observer()
    observer.schedule(event_handler,path,recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
if __name__ == "__main__":
    watch()
    