# PHOTOmosaic Generator

This repository provides a complete workflow to extract frames from a movie or video and use them to recreate a target image (such as a profile picture).
The included Python script has been upgraded to automatically detect the aspect ratio of your video frames (preventing squished or distorted tiles) and features a dynamic scaling argument to generate massive, high-resolution mosaics where individual frames remain crisp when zoomed in.
Prerequisites
Before running the scripts, ensure you have the following installed:
Python 3.x
FFmpeg: Required for extracting frames from your source video.
Python Libraries:
Install the required libraries using pip:
```bash
   pip install opencv-python numpy
   ```
Step 1: Extract Frames from Video
Use FFmpeg to extract frames from your video file. It is recommended to extract 1 frame per second to avoid duplicate frames and save storage space.
Create a folder for your frames and run the following command. (This example uses NVIDIA CUDA hardware acceleration for HEVC/x265 video. Remove `-hwaccel cuda` if you do not have an NVIDIA GPU).
```bash
mkdir frames
ffmpeg -hwaccel cuda -i "Your_Movie_File.mkv" -r 1 frames/frame_%05d.jpg
```
Optional: Square Frames
If you want your mosaic grid to be built using perfect squares instead of the movie's native widescreen aspect ratio, you can tell FFmpeg to crop the center of the video during extraction:
```bash
mkdir frames_square
ffmpeg -hwaccel cuda -i "Your_Movie_File.mkv" -vf "crop=ih:ih" -r 1 frames_square/frame_%05d.jpg
```
Step 2: Generate the Photomosaic
Once your frames are extracted, use `photomosaic.py` to stitch them into your target image. The script will automatically read the first image in your pool, calculate its aspect ratio, and apply it to the entire grid.
Basic Usage
```bash
python photomosaic.py --input target_image.jpg --pool frames --output final_mosaic.jpg --stride 20
```
Advanced Usage (High Resolution)
If your output image looks too blurry when zooming in to see the individual movie frames, use the `--scale` parameter. This multiplies the overall canvas resolution while keeping your exact grid layout intact.
```bash
python photomosaic.py --input target_image.jpg --pool "C:\path\to\frames" --output final_mosaic.jpg --stride 20 --scale 5
```
Arguments
`--input` : Path to your target image (e.g., your profile picture). Default is `data/input.jpg`.
`--output` : Path and filename for the final generated mosaic. Default is `data/output.jpg`.
`--pool` : Path to the folder containing your extracted movie frames. Default is `image_pool`. Can be a relative or absolute path.
`--stride` : The base size of the grid tiles. A lower number (e.g., 10) creates a highly detailed mosaic with thousands of tiny frames. A higher number (e.g., 50) uses larger frames but reduces the overall detail of the target image.
`--scale` : (Optional) Multiplier to upscale the final resolution of the mosaic. For example, `--scale 5` will output an image 5 times larger than your input image, keeping individual frames sharp when zoomed in. Default is `1`.
Troubleshooting
ValueError: operands could not be broadcast together...
This means the script found zero images in your pool folder. Double-check your `--pool` path. If relative paths fail, use the full absolute path enclosed in quotes (e.g., `--pool "C:\Users\Name\Desktop\frames"`).
The final image is unrecognizable:
Your stride is likely too high, or your input image is too low-resolution. Try lowering the `--stride` to 10 or 5, or manually upscale your target image in an image editor before running the script.
