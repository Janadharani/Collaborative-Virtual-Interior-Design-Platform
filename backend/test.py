import torch
from PIL import Image
from diffusers import StableDiffusionInpaintPipeline
import os

# File Paths (Keep original paths)
UPLOAD_IMAGE_PATH = r"S:/project/nitroware/room generation/backend/room.jpg"
OUTPUT_IMAGE_PATH = r"S:/project/nitroware/room generation/backend/output_with_furniture.jpg"
MASK_IMAGE_PATH = r"S:/project/nitroware/room generation/backend/mask.jpg"

# Load Model (Same as before)
print("Loading Stable Diffusion Inpainting model...")
inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained("runwayml/stable-diffusion-inpainting")
inpaint_pipe.to("cuda" if torch.cuda.is_available() else "cpu")
print("Model loaded successfully.")

# Image Loading (Same resizing)
print("Loading and resizing input image...")
image = Image.open(UPLOAD_IMAGE_PATH).convert("RGB")
image = image.resize((512, 512))

# Enhanced Mask Configuration
if os.path.exists(MASK_IMAGE_PATH):
    print("Loading mask image...")
    mask = Image.open(MASK_IMAGE_PATH).convert("L")
    mask = mask.resize((512, 512))
else:
    print("Creating optimized furniture placement mask...")
    mask = Image.new("L", (512, 512), color=0)
    # Expanded mask areas for different furniture zones
    draw = Image.new("L", (512, 512), color=0)
    # Main seating area
    for x in range(100, 400):
        for y in range(300, 450):
            draw.putpixel((x, y), 255)
    # Wall areas for shelves and storage
    for x in range(50, 150):
        for y in range(100, 400):
            draw.putpixel((x, y), 255)
    for x in range(350, 450):
        for y in range(100, 400):
            draw.putpixel((x, y), 255)
    # Center area for coffee table
    for x in range(200, 300):
        for y in range(250, 350):
            draw.putpixel((x, y), 255)
    mask.paste(draw, (0, 0))

# Enhanced Furniture Prompt
prompt = (
    "A beautifully designed room with modern furniture and decor: "
    "1. A large, comfortable sofa positioned centrally or along a wall, "
    "2. A sleek coffee table in front of the sofa, "
    "3. Elegant floor lamps for ambient lighting, "
    "4. A modern TV unit or entertainment center on a wall, "
    "5. Shelves or storage units with books and decorative items, "
    "6. A stylish rug adding warmth to the floor, "
    "7. Side tables with small lamps or decor, "
    "8. Potted plants strategically placed in corners or near furniture, "
    "9. Wall art or paintings to enhance the aesthetic appeal, "
    "10. Curtains or blinds on windows to complement the room's theme. "
    "Ensure a cohesive, functional layout with balanced spacing, modern styling, and realistic lighting."
)

# Add negative prompt to preserve structure
negative_prompt = (
    "empty space, messy layout, floating furniture, "
    "distorted walls, closed windows, poor lighting, unrealistic objects"
)

# Run Inpainting with Enhanced Parameters
print("Generating furnished room...")
result = inpaint_pipe(
    prompt=prompt,
    image=image,
    mask_image=mask,
    negative_prompt=negative_prompt,
    num_inference_steps=50,  # Increased for better detail
    guidance_scale=14.5,     # Stronger prompt adherence
).images[0]

# Save Output
result.save(OUTPUT_IMAGE_PATH)
print(f"Fully furnished room saved at: {OUTPUT_IMAGE_PATH}")
