from transformers import pipeline
from PIL import Image
def generate_map_depth(image_path, output_depth_path):
    depth_estimator=pipeline("depth-estimation", model="Intel/dpt-large")
    print(f"Analyzing image for depth estimation: {image_path}")
    imagine_color=Image.open(image_path)
    prediction=depth_estimator(imagine_color)
    depth_map=prediction["depth"]
    depth_map.save(output_depth_path)
    print(f"Depth map saved successfully at: {output_depth_path}")
    return True