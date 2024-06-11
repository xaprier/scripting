import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import argparse


def rotate_video(input_path, output_path, transpose_value):
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_path,
        "-vf",
        f"transpose={transpose_value}",
        "-c:a",
        "copy",
        output_path,
    ]
    subprocess.run(ffmpeg_command)


def process_videos_in_directory(directory, transpose_value):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    tasks = []
    with ThreadPoolExecutor() as executor:
        for file in files:
            # Check if the file is a .mp4 video
            if file.endswith(".mp4"):
                input_path = os.path.join(directory, file)
                # Create the output file name by appending "_2" before the file extension
                output_file = file.replace(".mp4", "_2.mp4")
                output_path = os.path.join(directory, output_file)

                # Submit the task to the thread pool
                tasks.append(
                    executor.submit(
                        rotate_video, input_path, output_path, transpose_value
                    )
                )

    # Wait for all tasks to complete
    for task in tasks:
        task.result()


def main():
    parser = argparse.ArgumentParser(
        description="Rotate all .mp4 videos in a directory."
    )
    parser.add_argument(
        "directory", help="The directory containing the videos to process."
    )
    parser.add_argument(
        "-t",
        "--transpose",
        type=int,
        choices=[0, 1, 2, 3],
        default=2,
        help="Transpose value for rotation: 0=90CounterCLockwise and Vertical Flip, 1=90Clockwise, 2=90CounterClockwise, 3=90Clockwise and Vertical Flip.",
    )

    args = parser.parse_args()

    process_videos_in_directory(args.directory, args.transpose)


if __name__ == "__main__":
    main()
