import os
import subprocess  
import cv2

def get_best_model_path(sparse_folder):
    if not os.path.exists(sparse_folder):
        print(f"Error: Sparse folder not found: {sparse_folder}")
        return None
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

def extract_extensions_frames(video_path, output_folder, prefix="video2_", frames_per_second=5):
    print(f"Extracting frames from video: {video_path}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video: {video_path}")
        return False
    original_fps=cap.get(cv2.CAP_PROP_FPS)
    frame_skip=int(round(original_fps / frames_per_second))
    current_frame=0
    saved_frames=0
    while True:
        ret, frame = cap.read()
        if not ret:
            break #end of video
        if current_frame % frame_skip == 0:
            original_height, original_thickness=frame.shape[:2] #4k render and crop
            bottom_limit=int(original_height*0.80)
            frame_crop=frame[0:bottom_limit, 0:original_thickness]
            scale_factor=1920.0/original_thickness
            new_height=int(frame_crop.shape[0]*scale_factor)
            final_frame=cv2.resize(frame_crop, (1920, new_height))
            image_name=f"{prefix}{saved_frames:04d}.jpg"
            cv2.imwrite(os.path.join(output_folder, image_name), final_frame)
            saved_frames+=1
        current_frame+=1
    cap.release()
    print(f"Finished extracting frames. Total saved frames: {saved_frames} into the folder: {output_folder}")
    return True

def run_colmap_extension(colmap_exe_path, workspace_folder, images_folder):
    database_path=os.path.join(workspace_folder, "database.db")
    sparse_path=os.path.join(workspace_folder, "sparse")
    input_model_path=get_best_model_path(sparse_path)
    if not input_model_path:
        print("Error: No valid COLMAP sparse model found for extension.")
        return False
    extended_output_path=os.path.join(workspace_folder, "sparse_extended")
    if not os.path.exists(extended_output_path):
        os.makedirs(extended_output_path)
        print(f"Created extended output folder: {extended_output_path}")
    try:
        print("Feature extraction for extension...")
        subprocess.run([
            colmap_exe_path, "feature_extractor",
            "--database_path", database_path,
            "--image_path", images_folder,
            "--ImageReader.single_camera", "1",
            "--ImageReader.camera_model", "SIMPLE_RADIAL",
        ], check=True)

        print("Exhaustive matching for extension...")
        subprocess.run([
            colmap_exe_path, "exhaustive_matcher",
            "--database_path", database_path,
        ], check=True)

        print(f"Running incremental mapper for (Starting from {input_model_path})...")
        subprocess.run([
            colmap_exe_path, "mapper",
            "--database_path", database_path,
            "--image_path", images_folder,
            "--input_path", input_model_path,       # starting from the best existing sparse model
            "--output_path", extended_output_path,  
            "--Mapper.init_min_tri_angle", "2.0",
            "--Mapper.multiple_models", "0",
            "--Mapper.ba_refine_focal_length", "1",
            "--Mapper.ba_refine_extra_params", "1"
        ], check=True)
        print("Extension mapping completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running COLMAP extension: {e}")
        return None
    

def convert_extended_to_ply(colmap_exe_path, extended_folder, output_ply_path):
    print(f"Converting COLMAP extended sparse model to PLY format using executable: {colmap_exe_path}")
    model_folder=get_best_model_path(extended_folder) or extended_folder
    try:
        subprocess.run([
            colmap_exe_path, "model_converter",
            "--input_path", model_folder,
            "--output_path", output_ply_path,
            "--output_type", "PLY",
        ], check=True)
        print("Conversion of extended model to PLY completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error converting extended model to PLY: {e}")
    
if __name__=="__main__":
    colmap_path = r"A:\LICENTA\COLMAP\colmap-x64-windows-cuda\COLMAP.bat"
    workspace_folder = "dataset"
    images_folder = os.path.join(workspace_folder, "images")
    output_ply = os.path.join(workspace_folder, "extended_model.ply")
    new_video="test2_1.mp4"
    #print("Extracting frames from new video for extension...")
    #extract_extensions_frames(new_video, images_folder, prefix="extension_", frames_per_second=5)
    extended_sparse_path=run_colmap_extension(colmap_path, workspace_folder, images_folder)
    if extended_sparse_path:
        convert_extended_to_ply(colmap_path, os.path.join(workspace_folder, "sparse_extended"), output_ply)
        print("\nSuccess! Extended Sparse Point Cloud was generated!")

    #convert_extended_to_ply(colmap_path, os.path.join(workspace_folder, "sparse_extended"), output_ply)
    #print("\nSuccess! Extended Sparse Point Cloud was generated!")
    
