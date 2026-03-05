from video_processor import extract_frames_for_sfm
from sfm_processor import run_colmap_dense_reconstruction, run_colmap_sfm, convert_sparse_to_ply
import os

def main():
    video_test="test_video.mp4"
    workspace_folder="dataset"
    images_folder=os.path.join(workspace_folder, "images")
    sparse_folder=os.path.join(workspace_folder, "sparse")
    output_ply=os.path.join(workspace_folder, "sparse_model.ply")
    colmap_path=r"A:\LICENTA\COLMAP\colmap-x64-windows-cuda\COLMAP.bat"
    print("Extracting frames from video for SfM...")
    extract_frames_for_sfm(video_test, images_folder, frames_per_second=5)
    succes_sfm=run_colmap_sfm(colmap_path, workspace_folder, images_folder)
    if succes_sfm:
        print("Converting COLMAP sparse model to PLY format...")
        convert_sparse_to_ply(colmap_path, sparse_folder, output_ply)
        print("Starting COLMAP dense reconstruction...")
        run_colmap_dense_reconstruction(colmap_path, workspace_folder)
    else:
        print("SfM failed. Skipping dense reconstruction.")

if __name__=="__main__":    main()