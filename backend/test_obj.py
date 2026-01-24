# Step 1: Install Required Libraries (Run in Terminal if not installed)
# pip install ultralytics opencv-python

# Step 2: Import Required Libraries
import torch
from ultralytics import YOLO
import cv2
import os
import shutil

# Step 3: Load the Trained YOLOv8 Model
model_path = "S:/project/nitroware/room generation/backend/best.pt"  # Update with your model path

if not os.path.exists(model_path):
    print("❌ Error: Trained model not found! Ensure 'best.pt' is in the correct folder.")
    exit()
else:
    print("✅ Model loaded successfully!")

model = YOLO(model_path)  # Load YOLOv8 model

# Step 4: Set Paths for Testing
single_image_path = "S:/project/nitroware/room generation/backend/test_images/image.png"  # Specific image path
output_path = "S:/project/nitroware/room generation/backend/output_images/"  # Directory to save results

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

# Clear previous YOLO detection results
yolo_results_path = "runs/detect/predict"
if os.path.exists(yolo_results_path):
    shutil.rmtree(yolo_results_path)  # Delete previous runs to avoid confusion

# Step 5: Preprocess Image for Detection
def preprocess_image(image_path, upscale_factor=2):
    """Preprocess the image by upscaling to improve YOLOv8 detection."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Error: Unable to read image at {image_path}")
        return None

    # Adjust brightness and contrast
    alpha = 1.2  # Brightness control (1.0 - 3.0)
    beta = 30    # Contrast control (0-100)
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # Upscale the image
    height, width = img.shape[:2]
    new_width, new_height = width * upscale_factor, height * upscale_factor
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    print(f"🔄 Image upscaled to: {new_width}x{new_height}")
    return resized_img

# Step 6: Run Object Detection on Preprocessed Image
if os.path.exists(single_image_path):
    print(f"🔍 Running furniture detection on single image: {single_image_path}")

    # Preprocess the image
    preprocessed_img = preprocess_image(single_image_path, upscale_factor=2)
    if preprocessed_img is not None:
        # Save the preprocessed image temporarily
        temp_image_path = "temp_upscaled_image.jpg"
        cv2.imwrite(temp_image_path, preprocessed_img)

        # Run YOLO detection with very low confidence and high resolution
        results = model.predict(source=temp_image_path, save=True, conf=0.31, imgsz=640)

        # Move output image to output directory
        detected_img_name = os.path.basename(single_image_path)  # Keep original image name
        detected_img_path = os.path.join(yolo_results_path, os.path.basename(temp_image_path))
        output_img_path = os.path.join(output_path, detected_img_name)

        if os.path.exists(detected_img_path):
            shutil.move(detected_img_path, output_img_path)  # Move detected image to output directory
            print(f"✅ Furniture detected and saved: {output_img_path}")

            # Load and Show Image using OpenCV
            img = cv2.imread(output_img_path)
            cv2.imshow("Furniture Detection", img)
            cv2.waitKey(0)  # Wait for a key press
            cv2.destroyAllWindows()
        else:
            print("⚠️ No furniture detected in the image.")

        # Cleanup temporary files
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
else:
    print("❌ Error: Single image not found. Check the path provided.")
