from file_handler import load_photos_from_directory

images = load_photos_from_directory("/Users/danielashpes/Desktop/test_photos")
for img in images:
    print(img["file_path"])
    img["thumbnail"].show()