from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from PIL.ImageQt import ImageQt

class PhotoGallery(QMainWindow):
    def __init__(self, images):
        super().__init__()
        self.setWindowTitle("Photo Gallery")
        self.images = images
        self.current_image = None  # Track the current image path
        self.gallery_widget = None
        self.init_ui()  # Initialize the UI immediately

    def load_thumbnail(self, image_path, thumbnail_label):
        """ Load a single thumbnail asynchronously. """
        def update_thumbnail():
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            thumbnail_label.setPixmap(pixmap)
        
        # Ensure the event loop is processed immediately after adding the thumbnail
        QApplication.processEvents()
        QTimer.singleShot(0, update_thumbnail)

    def init_ui(self):
        """ Initializes the gallery view UI. """
        self.gallery_widget = QWidget(self)
        self.setCentralWidget(self.gallery_widget)

        # Gallery layout
        self.layout = QGridLayout(self.gallery_widget)
        row, col = 0, 0

        for img_data in self.images:
            thumbnail_path = img_data["file_path"]  # Assuming 'file_path' is the actual image path
            qt_image = ImageQt(img_data["thumbnail"])  # Assuming 'thumbnail' is a PIL image

            # Create a label to hold the thumbnail
            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Load the thumbnail asynchronously
            self.load_thumbnail(thumbnail_path, label)

            # Connect the click event to show the full image
            label.mousePressEvent = lambda event, path=img_data["file_path"]: self.show_full_image(path)

            # Add the label to the grid layout
            self.layout.addWidget(label, row, col)

            col += 1
            if col >= 4:  # 4 thumbnails per row
                col = 0
                row += 1

        # Make sure the gallery layout is displayed immediately
        self.gallery_widget.setLayout(self.layout)

    def show_full_image(self, image_path):
        """ Switches to full-image view in the same window with a Back button. """
        print(f"Clicked on: {image_path}")  # Debugging line to check if the function is called
        self.current_image = image_path  # Store the current image path

        # Clear the gallery layout (optional, depending on your UI design)
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create a new widget for full image view
        self.image_widget = QWidget(self)
        self.setCentralWidget(self.image_widget)

        # Full image layout
        full_image_layout = QVBoxLayout(self.image_widget)

        # Load the full image and display it
        pixmap = QPixmap(image_path)
        if pixmap.isNull():  # Debugging: Check if the image is loaded correctly
            print("Failed to load the image")
        
        # Scale the image to fit within the window while preserving the aspect ratio
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel()
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a text widget for displaying metadata
        from backend.file_handler import get_metadata
        metadata_text = get_metadata(image_path)
        metadata_label = QTextEdit()
        metadata_label.setText(metadata_text)
        metadata_label.setReadOnly(True)

        # Back button to return to gallery
        back_button = QPushButton("Back to Gallery")
        back_button.clicked.connect(self.return_to_gallery)

        # Add full image, metadata, and back button to the layout
        full_image_layout.addWidget(label)
        full_image_layout.addWidget(metadata_label)
        full_image_layout.addWidget(back_button)

        self.image_widget.setLayout(full_image_layout)

    def return_to_gallery(self):
        """ Returns to the gallery view. """
        self.init_ui()  # Re-initialize the gallery layout


# Create the application and window
app = QApplication([])
window = PhotoGallery(images=[])  # Pass in the list of images with their data (path, thumbnail, etc.)
window.show()

# Run the application
app.exec()