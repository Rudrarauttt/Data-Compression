import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QStyle
import lzma
import os

class FileCompressorDecompressor(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.compress_button = QPushButton("Compress File", self)
        self.compress_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.compress_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.decompress_button = QPushButton("Decompress File", self)
        self.decompress_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.decompress_button.setStyleSheet("background-color: #2196F3; color: white;")
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: green")
        self.status_label = QLabel("Ready")
        self.original_size_label = QLabel("Original Size: ", self)
        #self.original_size_label.move(10, 70)
        self.compressed_size_label = QLabel("Compressed Size: ", self)
        #self.compressed_size_label.move(240, 70)
        

        
        

        self.compress_button.clicked.connect(self.compress_file)
        self.decompress_button.clicked.connect(self.decompress_file)

        layout = QVBoxLayout()
        layout.addWidget(self.compress_button)
        layout.addWidget(self.decompress_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.original_size_label)
        layout.addWidget(self.compressed_size_label)
        


        self.setLayout(layout)

    def compress_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a file to compress""", "All Files (*)")
        if file_path:
            compressed_file_path = file_path + ".zip"
            original_size = os.path.getsize(file_path) / 1024
            try:
                with open(file_path, 'rb') as f_in, lzma.open(compressed_file_path, 'wb') as f_out:
                    f_out.write(f_in.read())
                compressed_size = os.path.getsize(compressed_file_path) / 1024
                self.status_label.setText(f"File compressed to {compressed_file_path}")
                self.status_label.setStyleSheet("color: green")
                self.original_size_label.setText(f"Original Size: {original_size:.2f} KB")
                self.compressed_size_label.setText(f"Compressed Size: {compressed_size:.2f} KB")
            except Exception as e:
                self.status_label.setText(f"Compression failed: {str(e)}")
                self.status_label.setStyleSheet("color: red")

    def decompress_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a compressed file to decompress", filter="*.")
        if file_path:
            try:
                decompressed_file_path = file_path[:-3]
                compressed_size = os.path.getsize(file_path) / 1024  
                with lzma.open(file_path, 'rb') as f_in, open(decompressed_file_path, 'wb') as f_out:
                    f_out.write(f_in.read())
                self.status_label.setText(f"File decompressed to {decompressed_file_path}")
                self.status_label.setStyleSheet("color: green")
                self.original_size_label.setText(f"Original Size: {original_size:.2f} KB")
                self.compressed_size_label.setText(f"Compressed Size: {compressed_size:.2f} KB")
            except Exception as e:
                self.status_label.setText(f"Decompression failed: {str(e)}")
                self.status_label.setStyleSheet("color: red")

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    app.setStyle("Fusion")  
    window.setCentralWidget(FileCompressorDecompressor())
    window.setWindowTitle("File Compression and Decompression")
    window.setGeometry(100, 100, 400, 150)
    window.show()
    sys.exit(app.exec_())
