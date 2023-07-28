import cv2
import os
import argparse

def create_video_from_screenshots(image_folder, output_video_path, fps):
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png'):
            img_path = os.path.join(image_folder, filename)
            images.append(cv2.imread(img_path))

    if len(images) == 0:
        print("No images found in the specified folder.")
        return

    height, width, _ = images[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for image in images:
        video_writer.write(image)

    video_writer.release()
    print(f"Video created successfully: {output_video_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create video from screenshots')
    parser.add_argument('--image_folder', type=str, help='Path to the image folder')
    parser.add_argument('--output_video_path', type=str, help='Path to the output video file')
    parser.add_argument('--fps', type=float, help='Frames per second for the video')

    args = parser.parse_args()

    image_folder = args.image_folder
    output_video_path = args.output_video_path
    fps = args.fps

    create_video_from_screenshots(image_folder, output_video_path, fps)