from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL.ImageQt import ImageQt

#  Test the functionality
def main():
    app = QApplication([])
    from backend.file_handler import load_photos_from_directory  # Import the function if it's in another file
    from ui.photo_gallery_corrected import PhotoGallery

    images = load_photos_from_directory("/Users/danielashpes/Desktop/test_photos")
    gallery = PhotoGallery(images)
    gallery.show()
    app.exec()


if __name__ == "__main__":
    main()