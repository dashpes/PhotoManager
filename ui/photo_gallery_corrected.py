from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QGridLayout, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QTextEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL.ImageQt import ImageQt


class PhotoGallery(QMainWindow):
    def __init__(self, images):
        super().__init__()
        self.setWindowTitle("Photo Gallery")
        self.images = images
        self.current_image = None  # Track the current image path

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        """Initializes the gallery view UI."""
        self.gallery_widget = QWidget(self)
        self.setCentralWidget(self.gallery_widget)

        # Gallery layout
        layout = QGridLayout(self.gallery_widget)
        row, col = 0, 0

        for img_data in self.images:
            thumbnail = img_data["thumbnail"]
            qt_image = ImageQt(thumbnail)
            pixmap = QPixmap.fromImage(qt_image)

            # Create a label to hold the thumbnail
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.mousePressEvent = lambda event, path=img_data["file_path"]: self.show_full_image(path)
            layout.addWidget(label, row, col)

            col += 1
            if col >= 4:  # 4 thumbnails per row
                col = 0
                row += 1

    def show_full_image(self, image_path):
        """Switches to full-image view in the same window with a Back button."""
        print(f"Clicked on: {image_path}")  # Debugging line to check if the function is called
        self.current_image = image_path  # Store the current image path

        # Clear the gallery layout
        self.gallery_widget.deleteLater()
        self.image_widget = QWidget(self)
        self.setCentralWidget(self.image_widget)

        # Full image layout
        layout = QVBoxLayout(self.image_widget)

        # Back button layout
        back_button = QPushButton("Back to Gallery")
        back_button.clicked.connect(self.return_to_gallery)
        back_button.setMaximumWidth(150)  # Adjust size if needed
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Horizontal layout for image and metadata
        content_layout = QHBoxLayout()

        # Left-side layout: Image
        pixmap = QPixmap(image_path)
        if pixmap.isNull():  # Debugging: Check if the image is loaded correctly
            print("Failed to load the image")

        # Resize the pixmap to fit within reasonable bounds
        max_width, max_height = 1000, 800
        pixmap = pixmap.scaled(
            max_width, max_height, Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation  # Use smooth transformation for better quality
        )
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left_layout = QVBoxLayout()
        left_layout.addWidget(label)

        # Right-side layout: Metadata
        from backend.file_handler import get_metadata
        metadata_text = get_metadata(image_path)
        metadata_label = QTextEdit()
        metadata_label.setText(metadata_text)
        metadata_label.setReadOnly(True)

        right_layout = QVBoxLayout()
        right_layout.addWidget(metadata_label)

        # Add image and metadata to the content layout
        content_layout.addLayout(left_layout)
        content_layout.addLayout(right_layout)

        # Add content layout to the main layout
        layout.addLayout(content_layout)

    def return_to_gallery(self):
        """Returns to the gallery view."""
        self.init_ui()  # Re-initialize the gallery layout
