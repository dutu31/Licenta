import subprocess
import os
def run_colmap_sfm(colmap_exe_path, workspace_folder, images_folder):
    print(f"Running COLMAP SfM with executable: {colmap_exe_path}")
    database_path=os.path.join(workspace_folder, "database.db")
    sparse_path=os.path.join(workspace_folder, "sparse")
    if not os.path.exists(sparse_path):
        os.makedirs(sparse_path)
        print(f"Created sparse output folder: {sparse_path}")
    try:
        # Step 1: Feature extraction
        cmd_extract=[
            colmap_exe_path, "feature_extractor",
            "--database_path", database_path,
            "--image_path", images_folder,
            "--ImageReader.single_camera", "1",
            "--ImageReader.camera_model", "SIMPLE_RADIAL",
        ]
        subprocess.run(cmd_extract, check=True)
        print("Feature extraction completed successfully.")
        # Step 2: Sequential matching
        cmd_match=[
            colmap_exe_path, "sequential_matcher",
            "--database_path", database_path,
            "--SequentialMatching.overlap", "15",       
            "--SequentialMatching.loop_detection", "1"
        ]
        subprocess.run(cmd_match, check=True)
        print("Sequential matching completed successfully.")
        # Step 3: Mapper 
        cmd_mapper=[
            colmap_exe_path, "mapper",
            "--database_path", database_path,
            "--image_path", images_folder,
            "--output_path", sparse_path,
            "--Mapper.init_min_tri_angle", "1.5",            
            "--Mapper.tri_min_angle", "1.5",                 
            "--Mapper.filter_min_tri_angle", "1.5",          
            "--Mapper.multiple_models", "0",
            "--Mapper.abs_pose_min_num_inliers", "15",       
            "--Mapper.abs_pose_min_inlier_ratio", "0.05",
            "--Mapper.ba_refine_focal_length", "0",          #no zoom
            "--Mapper.ba_refine_extra_params", "0"
        ]
        subprocess.run(cmd_mapper, check=True)
        print("Mapping completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running COLMAP SfM: {e}")
        return False

def convert_sparse_to_ply(colmap_exe_path, sparse_folder, output_ply_path):
    print(f"Converting COLMAP sparse model to PLY format using executable: {colmap_exe_path}")
    model_folder=os.path.join(sparse_folder, "0")
    if not os.path.exists(model_folder):
        print(f"Error: COLMAP sparse model folder not found: {model_folder}")
        print("Mapper may not have run successfully or output is in a different location.")
        return False
    command=[
        colmap_exe_path, "model_converter",
        "--input_path", model_folder,
        "--output_path", output_ply_path,
        "--output_type", "PLY"
    ]
    try:
        print("Converting sparse model to PLY format...")
        subprocess.run(command, check=True)
        print(f"Conversion completed successfully. Output PLY file: {output_ply_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting sparse model to PLY: {e}")
        return False
    

def run_colmap_dense_reconstruction(colmap_exe_path, workspace_folder):
    print(f"Running COLMAP dense reconstruction with executable: {colmap_exe_path}")
    sparse_folder=os.path.join(workspace_folder, "sparse", "0")
    images_folder=os.path.join(workspace_folder, "images")
    dense_folder=os.path.join(workspace_folder, "dense")
    if not os.path.exists(dense_folder):
        os.makedirs(dense_folder)
        print(f"Created dense output folder: {dense_folder}")
    if not os.path.exists(sparse_folder):
        print(f"Error: COLMAP sparse model folder not found: {sparse_folder}")
        print("Mapper may not have run successfully or output is in a different location.")
        return False
    try:
        cmd_undistort=[
            colmap_exe_path, "image_undistorter",
            "--image_path", images_folder,
            "--input_path", sparse_folder,
            "--output_path", dense_folder,
            "--output_type", "COLMAP"
        ]
        subprocess.run(cmd_undistort, check=True)
        print("Image undistortion completed successfully.")
        # Step 2: PatchMatch stereo
        cmd_patchmatch=[
            colmap_exe_path, "patch_match_stereo",
            "--workspace_path", dense_folder,
            "--workspace_format", "COLMAP",
            "--PatchMatchStereo.geom_consistency", "1", #enable geometric consistency check to improve depth map quality
            "--PatchMatchStereo.filter", "1", #enable filtering of depth maps to remove outliers and improve quality
            
        ]
        subprocess.run(cmd_patchmatch, check=True)
        print("PatchMatch stereo completed successfully.")
        # Step 3: Stereo fusion
        output_ply=os.path.join(dense_folder, "dense_model.ply")
        cmd_fusion=[
            colmap_exe_path, "stereo_fusion",
            "--workspace_path", dense_folder,
            "--workspace_format", "COLMAP",
            "--input_type", "geometric",
            "--output_path", output_ply,

            "--StereoFusion.min_num_pixels", "2",
            "--StereoFusion.max_reproj_error", "4",
            "--StereoFusion.max_depth_error", "3",
            "--StereoFusion.max_normal_error", "10"
        ]
        subprocess.run(cmd_fusion, check=True)
        print("Stereo fusion completed successfully. Output fused point cloud: dense_model.ply")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running COLMAP dense reconstruction: {e}")
        return False