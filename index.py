# Import necessary libraries
import os

# Define the dataset directory
# Replace this with the path to your labels directory in Google Drive
LABELS_DIR = r"S:\project\nitroware\room generation\furniture detection datase\furnitures\train\sofa\labels"

# Define the target class to replace (e.g., 0) and the new class (e.g., 3)
OLD_CLASS = 3
NEW_CLASS = 4

def update_labels(labels_dir, old_class, new_class):
    """
    Update the class labels in all label files in the specified directory.

    Args:
        labels_dir (str): Path to the directory containing label files.
        old_class (int): Class to be replaced.
        new_class (int): New class to assign.
    """
    # Ensure the labels directory exists
    if not os.path.exists(labels_dir):
        print(f"Error: Directory {labels_dir} does not exist.")
        return

    # Iterate over all label files in the directory
    for filename in os.listdir(labels_dir):
        if filename.endswith('.txt'):  # Process only .txt files
            file_path = os.path.join(labels_dir, filename)

            # Read the label file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Modify the class in each line
            updated_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:  # Ensure valid label format
                    class_id = int(parts[0])
                    if class_id == old_class:
                        parts[0] = str(new_class)  # Update class
                    updated_lines.append(' '.join(parts))

            # Write the updated labels back to the file
            with open(file_path, 'w') as file:
                file.write('\n'.join(updated_lines) + '\n')

            print(f"Updated: {filename}")

# Call the function to update labels
update_labels(LABELS_DIR, OLD_CLASS, NEW_CLASS)
print("Class label update completed.")