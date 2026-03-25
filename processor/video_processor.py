import cv2
import os
def extract_frames_for_sfm(video_path, output_folder, frames_per_second=2):
    print(f"Extracting frames from video: {video_path}")
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return False
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video: {video_path}")
        return False
    original_fps=cap.get(cv2.CAP_PROP_FPS)
    total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Original video FPS: {original_fps}, Total frames: {total_frames}")
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
            image_name=f"image_{saved_frames:04d}.jpg"
            saved_path=os.path.join(output_folder, image_name)
            cv2.imwrite(saved_path, final_frame)
            saved_frames+=1
        current_frame+=1
    cap.release()
    print(f"Finished extracting frames. Total saved frames: {saved_frames} into the folder: {output_folder}")
    return True