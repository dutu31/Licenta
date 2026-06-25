import os
import subprocess
import shutil # for file operations
import cv2
import sqlite3
import numpy as np
from ultralytics import YOLO

colmap_exe_path=r"A:\LICENTA\COLMAP\colmap-x64-windows-cuda\COLMAP.bat"
workspace_folder=r"dataset"
query_image_path=r"dataset\query\query_test.png"
cropped_image_path=r"dataset\query\query_test_cropped.png"

def get_best_model_path(sparse_folder):
    if not os.path.exists(sparse_folder):
        print(f"Error: Sparse folder not found: {sparse_folder}")
        return None
    if os.path.exists(os.path.join(sparse_folder, "points3D.bin")) or os.path.exists(os.path.join(sparse_folder, "points3D.txt")):
        return sparse_folder
    subdirs = [os.path.join(sparse_folder, d) for d in os.listdir(sparse_folder) if os.path.isdir(os.path.join(sparse_folder, d)) and d.isdigit()]
    if not subdirs:
        print(f"Error: No valid sparse model subdirectories found in: {sparse_folder}")
        return None
    best_model=None
    max_size=-1
    for subdir in subdirs:
        points_bin=os.path.join(subdir, "points3D.bin")
        points_txt=os.path.join(subdir, "points3D.txt")
        size=0
        if os.path.exists(points_bin):
            size=os.path.getsize(points_bin)
        elif os.path.exists(points_txt):
            size=os.path.getsize(points_txt)
        if size > max_size:
            max_size=size
            best_model=subdir
    return best_model if best_model else subdirs[0]

def resize_query_image(img_path, output_path):
    img=cv2.imread(img_path)
    if img is None:
        print(f"Error: Can't find image {img_path}!")
        return False
    original_height, original_thickness=img.shape[:2] #4k render and crop
    bottom_limit=int(original_height*0.80)
    img_crop=img[0:bottom_limit, 0:original_thickness]
    scale_factor=1920.0/original_thickness
    new_height=int(img_crop.shape[0]*scale_factor)
    img_final=cv2.resize(img_crop, (1920, new_height))
    cv2.imwrite(output_path, img_final)
    return True

def create_yolo_mask(image_path, mask_dir):
    model=YOLO("yolov8n-seg.pt")
    img=cv2.imread(image_path)
    h,w=img.shape[:2]
    mask=np.ones((h,w), dtype=np.uint8)*255
    results=model(image_path, verbose=False)
    if results[0].masks is not None:
        for i, mask_data in enumerate(results[0].masks.data):
            class_id=int(results[0].boxes.cls[i].item())
            #ignoring id for this classes
            ignorance_classes=[0, 1, 2, 3, 5, 7] #person, bicycle, car, motorcycle, bus, truck
            if class_id in ignorance_classes:
                m=mask_data.cpu().numpy()
                m_resized=cv2.resize(m, (w,h), interpolation=cv2.INTER_NEAREST)
                mask[m_resized>0]=0
    base_name=os.path.basename(image_path)
    mask_name=base_name + ".png"
    mask_path=os.path.join(mask_dir, mask_name)
    cv2.imwrite(mask_path, mask)
    print(f"Mask created and saved to {mask_path}")
    return mask_path


def localize_image(colmap_exe, workspace, query_image):
    database_path = os.path.join(workspace, "database.db")
    images_folder= os.path.join(workspace, "images")
    masks_folder= os.path.join(workspace, "masks")
    extended_dir= os.path.join(workspace, "sparse_extended")
    sparse_input= get_best_model_path(extended_dir)
    if sparse_input is None:
        print("Error: No valid COLMAP sparse model found for localization.")
        return False
    sparse_output= os.path.join(workspace, "sparse_localized")
    text_output= os.path.join(workspace, "text_localized")

    if not os.path.exists(sparse_output):
        os.makedirs(sparse_output)
    if not os.path.exists(text_output):
        os.makedirs(text_output)
    if not os.path.exists(masks_folder):
        os.makedirs(masks_folder)
    safe_image_name="live_localization_query.png"
    dest_path=os.path.join(images_folder, safe_image_name)
    shutil.copy2(query_image, dest_path)
    print(f"Photo was moved and overwritten to {images_folder}")
    create_yolo_mask(dest_path, masks_folder)
    if os.path.exists(database_path):
        try:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute("SELECT image_id FROM images WHERE name=?", (safe_image_name,))
            row = cursor.fetchone()
            if row:
                img_id = row[0]
                cursor.execute("DELETE FROM images WHERE image_id=?", (img_id,))
                cursor.execute("DELETE FROM keypoints WHERE image_id=?", (img_id,))
                cursor.execute("DELETE FROM descriptors WHERE image_id=?", (img_id,))
                conn.commit()
                print(f"Cleared old cache for {safe_image_name} from COLMAP database.")
            conn.close()
        except Exception as e:
            print(f"Warning: Could not clean database cache: {e}")
    
    try:
        print("Extracting features with mask applied...")
        subprocess.run([
            colmap_exe,
            "feature_extractor",
            "--database_path", database_path,
            "--image_path", images_folder,
            "--ImageReader.mask_path", masks_folder,
            "--ImageReader.single_camera", "1",
            "--ImageReader.camera_model", "SIMPLE_RADIAL"
        ], check=True)
        print("Matching features...")
        subprocess.run([
            colmap_exe,
            "exhaustive_matcher",
            "--database_path", database_path
        ], check=True)
        print("Registering image...")
        subprocess.run([
            colmap_exe,
            "image_registrator",
            "--database_path", database_path,
            "--input_path", sparse_input,
            "--output_path", sparse_output
        ], check=True)
        print("Exporting results...")
        subprocess.run([
            colmap_exe,
            "model_converter",
            "--input_path", sparse_output,
            "--output_path", text_output,
            "--output_type", "TXT",
        ], check=True)
        print("Localization completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__": 
    is_resized = resize_query_image(query_image_path, cropped_image_path)
    if is_resized:
        localize_image(colmap_exe_path, workspace_folder, cropped_image_path)
    else:
        print("Process aborted because resizing failed")
        