import os

def remove_empty_labels_and_images(label_folder, image_folder, image_extensions=None):
    """
    Deletes empty YOLO label files and their corresponding images.
    
    Parameters:
    - label_folder: Path to the folder containing YOLO labels.
    - image_folder: Path to the folder containing images.
    - image_extensions: List of allowed image extensions (default: jpg, png, jpeg).
    """
    if image_extensions is None:
        image_extensions = [".jpg", ".jpeg", ".png"]  # Common image formats

    deleted_files = 0  # Counter to track deletions

    print(f"\nScanning label files in: {label_folder}\n")

    for filename in os.listdir(label_folder):
        if filename.endswith(".txt"):  # Process only label files
            label_path = os.path.join(label_folder, filename)

            # Read the label file and check if it's truly empty
            with open(label_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                stripped_lines = [line.strip() for line in lines]  # Remove spaces and newlines

            if not any(stripped_lines):  # If all lines are empty
                print(f"🔴 Empty label file detected: {filename}")

                # Delete the empty label file
                try:
                    os.remove(label_path)
                    print(f"✅ Deleted label file: {filename}")
                except Exception as e:
                    print(f"⚠️ Error deleting label file {filename}: {e}")

                # Look for corresponding images and delete them
                image_name = os.path.splitext(filename)[0]  # Remove .txt extension
                image_deleted = False

                for ext in image_extensions:
                    image_path = os.path.join(image_folder, image_name + ext)
                    if os.path.exists(image_path):  # Check if image exists
                        try:
                            os.remove(image_path)
                            print(f"✅ Deleted corresponding image: {image_name + ext}")
                            image_deleted = True
                            break  # Stop after deleting the first found image
                        except Exception as e:
                            print(f"⚠️ Error deleting image {image_name + ext}: {e}")

                if not image_deleted:
                    print(f"⚠️ No matching image found for {filename}")

                deleted_files += 1

    if deleted_files == 0:
        print("\n✅ No empty label files found. Nothing was deleted.")
    else:
        print(f"\n✅ Cleanup completed! {deleted_files} empty label files and corresponding images removed.")

# Set paths
base_path = r"S:\project\nitroware\room generation\furniture detection datase\furnitures\test\sofa"  # Change this to your dataset path
label_folder = os.path.join(base_path, "labels")
image_folder = os.path.join(base_path, "images")

# Run the function
remove_empty_labels_and_images(label_folder, image_folder)
