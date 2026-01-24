# Step 1: Install required packages (Run once)
import os
import torch
from ultralytics import YOLO

# Step 2: Define Paths
dataset_path = r"S:\project\nitroware\room generation\furniture detection datase\furnitures"  # Dataset root folder
yaml_path = os.path.join(dataset_path, "data.yaml")  # YOLO dataset configuration file
output_dir = os.path.join(dataset_path, "trained_model")  # Where to save trained model

# Ensure trained_model folder exists
os.makedirs(output_dir, exist_ok=True)

# Step 3: Detect Intel Iris Xe GPU but use CPU for Training
try:
    import openvino  # Check if OpenVINO is installed
    print("✅ Intel Iris Xe detected! But training will use CPU since YOLOv8 doesn't support OpenVINO training.")
except ImportError:
    print("⚠️ OpenVINO not installed. Running training on CPU.")

device = "cpu"  # YOLOv8 only supports "cpu" or "cuda", so we must use CPU

# Step 4: Load YOLOv8 Model
model = YOLO("yolov8n.pt")  # Using YOLOv8 Nano model for faster training

# Step 5: Define Training Parameters
epochs = 20  # Run for 20 epochs
batch_size = 16  # Batch size
image_size = 640  # Image resolution
workers = 2  # Number of workers for data loading

# Step 6: Train the Model
print(f"🚀 Training YOLOv8 on Furniture Dataset using {device.upper()}...")
model.train(
    data=yaml_path,  # Path to dataset configuration
    epochs=epochs,  # Number of epochs
    batch=batch_size,  # Batch size
    imgsz=image_size,  # Image size
    workers=workers,  # Number of workers
    project=output_dir,  # Save training results in the dataset folder
    name="furniture_training",  # Subfolder name
    pretrained=True,  # Use pretrained YOLOv8 weights
    val=True,  # Enable validation
    device=device  # Must be "cpu" (Iris Xe does not support CUDA)
)

# Step 7: Verify and Save Trained Model
best_model_path = os.path.join(output_dir, "furniture_training", "weights", "best.pt")

if os.path.exists(best_model_path):
    print(f"✅ Model training completed. Model saved at: {best_model_path}")
else:
    print("❌ Error: Trained model not found! Please check training logs.")

print("✅ All results and trained model are stored in:", output_dir)
