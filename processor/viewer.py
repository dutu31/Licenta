import open3d as o3d
import os
import numpy as np
def view_colmap_point_cloud(ply_file_path):
    print(f"Loading COLMAP point cloud from: {ply_file_path}")
    if not os.path.exists(ply_file_path):
        print(f"Error: PLY file not found at path: {ply_file_path}")
        return False
    pcd=o3d.io.read_point_cloud(ply_file_path)
    if len(pcd.points)==0:
        print("Error: Loaded point cloud is empty. Check if COLMAP reconstruction was successful and the PLY file is valid.")
        return False
    print(f"Point cloud loaded successfully. Number of points: {len(pcd.points)}")
    R=pcd.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    pcd.rotate(R, center=(0, 0, 0))
    print("Visualizing COLMAP point cloud...")
    vis=o3d.visualization.Visualizer()
    vis.create_window(window_name="COLMAP Sparse Point Cloud", width=800, height=600)
    vis.add_geometry(pcd)
    opt=vis.get_render_option()
    opt.background_color=np.asarray([0, 0, 0]) #dark background for better contrast
    opt.point_size=2.0
    vis.run()
    vis.destroy_window()
    return True

if __name__=="__main__":
    path_to_map=os.path.join("dataset", "sparse_model.ply")
    view_colmap_point_cloud(path_to_map)