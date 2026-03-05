import open3d as o3d
import cv2
import numpy as np

def generate_point_cloud(color_path, depth_path, output_ply_path):
    print(f"Generating point cloud from color image: {color_path} and depth map: {depth_path}")
    color_image = cv2.imread(color_path)
    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
    depth_image = cv2.imread(depth_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    depth_image=cv2.bilateralFilter(depth_image, 9, 75, 75) #apply bilateral filter to smooth the depth map while preserving edges
    depth_image[depth_image == 0] = 0.1
    true_depth=10000.0/depth_image
    true_depth[true_depth > 600] = 0
    true_depth=true_depth.astype(np.uint16)
    #depth_image_inverted=255 - depth_image #MiDaS produces depth maps where closer objects are darker, so we invert it for Open3D
    o3d_color=o3d.geometry.Image(color_image)
    o3d_depth=o3d.geometry.Image(true_depth)
    rgbd_image=o3d.geometry.RGBDImage.create_from_color_and_depth(
        o3d_color, 
        o3d_depth,
        depth_scale=100.0, 
        depth_trunc=40.0, 
        convert_rgb_to_intensity=False
    )
    #generate virtual camera
    height, width = color_image.shape[:2]
    intrinsics=o3d.camera.PinholeCameraIntrinsic(
        width,
        height,
        fx=800.0,
        fy=800.0,
        cx=width / 2.0,
        cy=height / 2.0
    )
    #point cloud generation
    pcd=o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsics)
    #flip point cloud to align with the camera's coordinate system
    pcd.transform([[1, 0, 0, 0],
                   [0, -1, 0, 0],
                   [0, 0, -1, 0],
                   [0, 0, 0, 1]])
    o3d.io.write_point_cloud(output_ply_path, pcd)
    print(f"Point cloud saved successfully at: {output_ply_path}")
    print("We open the point cloud for visualization...")
    o3d.visualization.draw_geometries([pcd])
    return True
