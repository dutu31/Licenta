import os
import subprocess
import shutil # for file operations
import cv2
import sqlite3

colmap_exe_path=r"A:\LICENTA\COLMAP\colmap-x64-windows-cuda\COLMAP.bat"
workspace_folder=r"dataset"
query_image_path=r"dataset\query\query_test.png"
cropped_image_path=r"dataset\query\query_test_cropped.png"

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

def localize_image(colmap_exe, workspace, query_image):
    database_path = os.path.join(workspace, "database.db")
    images_folder= os.path.join(workspace, "images")
    sparse_input= os.path.join(workspace, "sparse", "0")
    sparse_output= os.path.join(workspace, "sparse_localized")
    text_output= os.path.join(workspace, "text_localized")

    if not os.path.exists(sparse_output):
        os.makedirs(sparse_output)
    if not os.path.exists(text_output):
        os.makedirs(text_output)
    image_name=os.path.basename(query_image)
    dest_path=os.path.join(images_folder, image_name)
    shutil.copy2(query_image,dest_path)
    print(f"Photo was moved and overwritten to {images_folder}")
    if os.path.exists(database_path):
        try:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            cursor.execute("SELECT image_id FROM images WHERE name=?", (image_name,))
            row = cursor.fetchone()
            if row:
                img_id = row[0]
                cursor.execute("DELETE FROM images WHERE image_id=?", (img_id,))
                cursor.execute("DELETE FROM keypoints WHERE image_id=?", (img_id,))
                cursor.execute("DELETE FROM descriptors WHERE image_id=?", (img_id,))
                conn.commit()
                print(f"Cleared old cache for {image_name} from COLMAP database.")
            conn.close()
        except Exception as e:
            print(f"Warning: Could not clean database cache: {e}")
    
    try:
        print("Extracting features...")
        subprocess.run([
            colmap_exe,
            "feature_extractor",
            "--database_path", database_path,
            "--image_path", images_folder,
            "--ImageReader.single_camera", "1",
            "--ImageReader.camera_model", "SIMPLE_RADIAL",
        ], check=True)
        print("Matching features...")
        subprocess.run([
            colmap_exe,
            "exhaustive_matcher",
            "--database_path", database_path,
        ], check=True)
        print("Registrating image...")
        subprocess.run([
            colmap_exe,
            "image_registrator",
            "--database_path", database_path,
            "--input_path", sparse_input,
            "--output_path", sparse_output,
            "--Mapper.ba_refine_focal_length", "0",
            "--Mapper.ba_refine_extra_params", "0",
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
        