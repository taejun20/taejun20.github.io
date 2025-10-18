from PIL import Image
import os

# Directory containing PNG images
input_dir = "."
output_dir = "."

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

filename = "profile2.png"

# Open the image
img_path = os.path.join(input_dir, filename)
img = Image.open(img_path).convert("RGB")  # convert to RGB to save as JPEG

jpg_path = os.path.join(output_dir, f"profileImage2.jpg")
# Save as JPEG
img.save(jpg_path, "JPEG", quality=80)

print("✅ All PNGs converted to JPGs.")
