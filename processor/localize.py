import os
import subprocess
import shutil # for file operations

colmap_exe_path=r"A:\LICENTA\COLMAP\colmap-x64-windows-cuda\COLMAP.bat"
workspace_folder=r"dataset"
query_image_path=r"dataset\query\query_test.png"

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
    if not os.path.exists(dest_path):
        shutil.copy2(query_image, dest_path)
        print(f"Photo was moved to {images_folder}")
    
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
if __name__ == "__main__":    localize_image(colmap_exe_path, workspace_folder, query_image_path)
        