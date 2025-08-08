import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from uploader import upload_file

# Função que aguarda o arquivo estar pronto para leitura
def wait_for_file_ready(file_path, timeout=30):
    """Espera até o arquivo estar pronto para leitura (evita PermissionError)."""
    start_time = time.time()
    while True:
        try:
            with open(file_path, 'rb'):
                return True
        except PermissionError:
            if time.time() - start_time > timeout:
                return False
            time.sleep(1)

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)

        # Verifica se é .csv ou .mkv
        if file_name.endswith(".csv") or file_name.endswith(".mkv"):
            print(f"📁 Novo arquivo detectado: {file_path}")
            if wait_for_file_ready(file_path):
                upload_file(file_path)
            else:
                print(f"⛔ Timeout: Arquivo '{file_path}' não ficou pronto para leitura.")

def start_watcher(folder="input"):
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    print(f"👀 Monitorando a pasta: {folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()

object