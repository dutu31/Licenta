import open3d as o3d
import os
import numpy as np
def view_colmap_point_cloud(ply_file_path, camera_pose=None):
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

    if camera_pose is not None:
        print(f"Showing camera position at: {camera_pose}")
        sphere=o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
        sphere.translate(camera_pose)
        sphere.paint_uniform_color([1, 0, 0]) #red color for camera position
        sphere.rotate(R, center=(0, 0, 0))
        vis.add_geometry(sphere)

    opt=vis.get_render_option()
    opt.background_color=np.asarray([0, 0, 0]) #dark background for better contrast
    opt.point_size=2.0
    vis.run()
    vis.destroy_window()
    return True


#2. quaternion to rotation matrix
def qvec2rotmat(qvec):
    w, x, y, z = qvec
    return np.array([
        [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
         2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
         2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
        [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
         1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
         2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
        [2 * qvec[1] * qvec[3] - 2 * qvec[0] * qvec[2],
         2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
         1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

def get_camera_position(images_text_path, target_image_name):
    if not os.path.exists(images_text_path):
        print(f"Error: images.txt file not found at path: {images_text_path}")
        return None
    with open(images_text_path, 'r') as f:
        lines=f.readlines()
    for i in range(len(lines)):
        line=lines[i].strip()
        if line.startswith("#") or len(line)==0:
            continue
        parts=line.split()
        if parts[-1]==target_image_name:
            qvec=np.array([float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])])
            tvec=np.array([float(parts[5]), float(parts[6]), float(parts[7])])
            R_mat=qvec2rotmat(qvec)
            camera_center=-np.dot(R_mat.T, tvec)
            return camera_center
    print(f"Error: Target image name '{target_image_name}' not found in images.txt.")
    return None



if __name__=="__main__":
    path_to_map=os.path.join("dataset", "sparse_model.ply")
    images_text_path=os.path.join("dataset", "text_localized", "images.txt")
    target_image="query_test.png"
    camera_position=get_camera_position(images_text_path, target_image)
    view_colmap_point_cloud(path_to_map, camera_position)