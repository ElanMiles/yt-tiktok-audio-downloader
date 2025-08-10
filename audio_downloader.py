import sys
import os
from pathlib import Path
import yt_dlp
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog,
    QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished_ok = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url: str, out_dir: str):
        super().__init__()
        self.url = url
        self.out_dir = out_dir

    def run(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(Path(self.out_dir) / '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [self._progress_hook],
            'quiet': True,
            'no_warnings': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filepath = ydl.prepare_filename(info)
                if not filepath.endswith(('.mp3', '.m4a', '.opus', '.wav')):
                    ydl_opts_post = {
                        'format': 'bestaudio/best',
                        'outtmpl': str(Path(self.out_dir) / '%(title)s.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'quiet': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts_post) as ydl2:
                        info = ydl2.extract_info(self.url, download=True)
                        filepath = ydl2.prepare_filename(info).replace('.webm', '.mp3')
                self.finished_ok.emit(filepath)
        except Exception as e:
            self.error.emit(str(e))

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded * 100 / total)
                self.progress.emit(percent)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Downloader (TikTok / YouTube)")
        self.resize(500, 170)

        vbox = QVBoxLayout(self)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("URL:"))
        self.url_edit = QLineEdit()
        hbox1.addWidget(self.url_edit)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Save to:"))
        self.path_edit = QLineEdit(str(Path.home() / "Downloads"))
        hbox2.addWidget(self.path_edit)
        self.browse_btn = QPushButton("Select Folder")
        self.browse_btn.clicked.connect(self.choose_folder)
        hbox2.addWidget(self.browse_btn)
        vbox.addLayout(hbox2)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        vbox.addWidget(self.progress_bar)

        self.download_btn = QPushButton("Download Audio")
        self.download_btn.clicked.connect(self.start_download)
        vbox.addWidget(self.download_btn)

        self.worker = None

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a Folder")
        if folder:
            self.path_edit.setText(folder)

    def start_download(self):
        url = self.url_edit.text().strip()
        folder = self.path_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a video URL")
            return
        if not os.path.isdir(folder):
            QMessageBox.warning(self, "Error", "Invalid folder selected")
            return

        self.download_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.worker = DownloadThread(url, folder)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished_ok.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_success(self, filepath):
        self.download_btn.setEnabled(True)
        QMessageBox.information(self, "Done", f"File saved:\n{filepath}")

    def on_error(self, msg):
        self.download_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
