import os
import sys
import threading
from PyQt6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QPushButton,QTextEdit,QProgressBar,QFileDialog,QMessageBox
from PyQt6.QtCore import Qt,pyqtSignal,QObject
from PyQt6.QtGui import QFont,QPalette,QColor,QIcon
from yt_dlp import YoutubeDL
import importlib

ICONS_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons")
PLATFORMS={"YouTube":("youtube_downloader","videos_yt",os.path.join(ICONS_DIR,"youtube.png")),"TikTok":("tiktok_downloader","videos_tiktok",os.path.join(ICONS_DIR,"tik-tok.png")),"Instagram":("instagram_downloader","videos_instagram",os.path.join(ICONS_DIR,"instagram.png")),"Twitter/X":("twitter_downloader","videos_twitter",os.path.join(ICONS_DIR,"social-media.png")),"Twitch":("twitch_downloader","videos_twitch",os.path.join(ICONS_DIR,"twitch.png")),"PornHub":("pornhub_downloader","videos_pornhub",os.path.join(ICONS_DIR,"Pornhub-logo.png")),}

class ProgressSignals(QObject):progress=pyqtSignal(int);output=pyqtSignal(str);finished=pyqtSignal()

class DownloaderWorker(threading.Thread):
    def __init__(self,module_name,url,custom_dir=None):super().__init__();self.module_name=module_name;self.url=url;self.custom_dir=custom_dir;self.signals=ProgressSignals()
    def run(self):
        try:
            mod=importlib.import_module(self.module_name);dir_path=self.custom_dir or mod.DIR;os.makedirs(dir_path,exist_ok=True)
            ydl_opts={'outtmpl':os.path.join(dir_path,'%(title)s.%(ext)s'),'format':'bestvideo+bestaudio/best' if 'youtube' in self.module_name else 'best','merge_output_format':'mp4','writethumbnail':True,'concurrent_fragment_downloads':5,'progress_hooks':[self.progress_hook],'quiet':True,'no_warnings':True,'noprogress':False}
            with YoutubeDL(ydl_opts) as ydl:self.signals.output.emit(f"Downloading: {self.url}\n");ydl.download([self.url]);self.signals.output.emit("Done\n")
        except Exception as e:self.signals.output.emit(f"Error: {e}\n")
        finally:self.signals.finished.emit()
    def progress_hook(self,d):
        if d['status']=='downloading':
            percent_str=d.get('_percent_str','0%').strip('% ')
            try:percent=int(float(percent_str))
            except:percent=0
            self.signals.progress.emit(percent)
        elif d['status']=='finished':self.signals.progress.emit(100)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();self.setWindowTitle("Video Downloader");self.resize(800,550)
        central=QWidget();self.setCentralWidget(central);layout=QVBoxLayout(central);layout.setSpacing(12);layout.setContentsMargins(30,5,30,30)
        platform_layout=QHBoxLayout();platform_layout.addWidget(QLabel("Platform:"));self.platform_combo=QComboBox()
        for name,(_,_,icon_path) in PLATFORMS.items():icon=QIcon(icon_path) if os.path.exists(icon_path) else QIcon();self.platform_combo.addItem(icon,name)
        self.platform_combo.setFixedHeight(40);platform_layout.addWidget(self.platform_combo,1);layout.addLayout(platform_layout)
        url_layout=QHBoxLayout();url_layout.addWidget(QLabel("URL:"));self.url_input=QLineEdit();self.url_input.setPlaceholderText("Enter video, reel, post or playlist URL");self.url_input.setFixedHeight(40);url_layout.addWidget(self.url_input,1);layout.addLayout(url_layout)
        dir_layout=QHBoxLayout();dir_layout.addWidget(QLabel("Folder:"));self.dir_label=QLabel();self.dir_label.setWordWrap(True);dir_layout.addWidget(self.dir_label,1);self.browse_btn=QPushButton("Browse");self.browse_btn.setFixedWidth(130);self.browse_btn.clicked.connect(self.browse_folder);dir_layout.addWidget(self.browse_btn);layout.addLayout(dir_layout)
        self.download_btn=QPushButton("Download");self.download_btn.setFixedHeight(48);self.download_btn.setFont(QFont("Arial",13,QFont.Weight.Bold));self.download_btn.clicked.connect(self.start_download);layout.addWidget(self.download_btn)
        self.progress_bar=QProgressBar();self.progress_bar.setRange(0,100);self.progress_bar.setValue(0);self.progress_bar.setFixedHeight(36);self.progress_bar.setTextVisible(True);self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter);layout.addWidget(self.progress_bar)
        self.log=QTextEdit();self.log.setReadOnly(True);self.log.setFont(QFont("Consolas",10));layout.addWidget(self.log,1)
        self.update_default_folder();self.platform_combo.currentTextChanged.connect(self.on_platform_changed);self.apply_theme()
    def apply_theme(self):
        app=QApplication.instance();palette=QPalette();palette.setColor(QPalette.ColorRole.Window,QColor(15,25,45));palette.setColor(QPalette.ColorRole.WindowText,QColor(200,220,255));palette.setColor(QPalette.ColorRole.Base,QColor(25,35,65));palette.setColor(QPalette.ColorRole.Text,QColor(200,220,255));palette.setColor(QPalette.ColorRole.Button,QColor(35,55,95));palette.setColor(QPalette.ColorRole.ButtonText,QColor(220,240,255));palette.setColor(QPalette.ColorRole.Highlight,QColor(0,120,240));app.setPalette(palette);app.setStyleSheet("QComboBox,QLineEdit,QPushButton,QTextEdit,QProgressBar{border:2px solid #447;border-radius:8px;padding:8px;background-color:#334477;color:#ddf}QPushButton:hover{background-color:#4466aa}QPushButton:pressed{background-color:#5588cc}QProgressBar::chunk{background-color:#00aaff;border-radius:6px}QLabel{color:#cce}")
    def on_platform_changed(self):self.log.clear();self.progress_bar.setValue(0);self.update_default_folder()
    def update_default_folder(self):
        platform=self.platform_combo.currentText();_,folder,_=PLATFORMS[platform];path=os.path.join(os.path.dirname(os.path.abspath(__file__)),folder);self.dir_label.setText(path);self.custom_dir=None
    def browse_folder(self):
        folder=QFileDialog.getExistingDirectory(self,"Select Folder")
        if folder:self.dir_label.setText(folder);self.custom_dir=folder
        else:self.update_default_folder()
    def start_download(self):
        url=self.url_input.text().strip()
        if not url:QMessageBox.warning(self,"Error","Enter URL");return
        platform=self.platform_combo.currentText();module,_,_=PLATFORMS[platform]
        self.download_btn.setEnabled(False);self.log.clear();self.log.append(f"Starting: {platform} – {url}\n");self.progress_bar.setValue(0)
        worker=DownloaderWorker(module,url,self.custom_dir);worker.signals.progress.connect(self.progress_bar.setValue);worker.signals.output.connect(self.log.append);worker.signals.finished.connect(lambda:self.download_btn.setEnabled(True));worker.start()

if __name__=="__main__":
    app=QApplication(sys.argv);win=MainWindow();win.show();sys.exit(app.exec())