import subprocess
import os

colmap_path = r"A:\LICENTA\COLMAP\colmap-x64-windows-cuda\COLMAP.bat"
sparse_folder = os.path.join("dataset", "sparse")
output_ply = os.path.join("dataset", "sparse_model.ply")

def convert(colmap_exe, sparse_dir, output_file):
    model_folder = os.path.join(sparse_dir, "2") 
    cmd = [colmap_exe, "model_converter", "--input_path", model_folder, "--output_path", output_file, "--output_type", "PLY"]
    subprocess.run(cmd, check=True)
    print("GATA! S-a creat sparse_model.ply din folderul 2.")

convert(colmap_path, sparse_folder, output_ply)