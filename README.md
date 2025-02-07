# VR-Funscript-AI-Generator

This project is a Python-based tool for generating Funscript files from VR videos using Computer Vision (CV) and AI techniques. It leverages YOLO (You Only Look Once) object detection and custom tracking algorithms to automate the process of creating Funscript files for interactive devices.

Join the **Discord community** for discussions and support: [Discord Community](https://discord.gg/WYkjMbtCZA)

The necessary YOLO models will also be available via the Discord.

---

## DISCLAIMER

This project is at its very early stages of development, still faulty and broken, and is for research and educational purposes only. It is not intended for commercial use.
Please, do not use this project for any commercial purposes without prior consent from the author. It is for individual use only.

---

## Features

- **YOLO Object Detection**: Uses a pre-trained YOLO model to detect and track objects in video frames.
- **Funscript Generation**: Generates Funscript data based on the tracked objects' movements.
- **Scene Change Detection**: Automatically detects scene changes in the video to improve tracking accuracy.
- **Visualization**: Provides real-time visualization of object tracking and Funscript data (in test mode).
- **VR Support**: Optimized for VR videos, with options to process specific regions of the frame.

---

## Project Genesis and Evolution

This project started as a dream to automate Funscript generation for VR videos. Here’s a brief history of its development:

- **Initial Approach (OpenCV Trackers)**: The first version relied on OpenCV trackers to detect and track objects in the video. While functional, the approach was slow (8–20 FPS) and struggled with occlusions and complex scenes.

- **Transition to YOLO**: To improve accuracy and speed, the project shifted to using YOLO object detection. A custom YOLO model was trained on a dataset of VR video frames, significantly improving detection quality. The new approach runs at 90 FPS on a Mac mini M4 pro, making it much more efficient.

- **Original Post**: For more details and discussions, check out the original post on EroScripts:  
[VR Funscript Generation Helper (Python + CV/AI)](https://discuss.eroscripts.com/t/vr-funscript-generation-helper-python-now-cv-ai/202554)

---

## YOLO Model

The YOLO model used in this project is based on YOLOv11n, which was fine-tuned with 10 new classes and 4,500+ frames randomly extracted from a VR video library. Here’s how the model was developed:

- **Initial Training**: A few hundred frames were manually tagged and boxed to create an initial dataset. The model was trained on this dataset to generate preliminary detection results.
- **Iterative Improvement**: The trained model was used to suggest bounding boxes in additional frames. The suggested boxes were manually adjusted, and the dataset was expanded. This process was repeated iteratively to improve the model’s accuracy.
- **Final Training**: After gathering 4,500+ images and 30,149 annotations, the model was trained for 200 epochs. YOLOv11s and YOLOv11m were also tested, but YOLOv11n was chosen for its balance of accuracy and inference speed.
- **Hardware**: The model runs on a Mac using MPS (Metal Performance Shaders) for accelerated inference on ARM chips. Other versions of the model (ONNX and PT) are also available for use on other platforms.

---

## Pipeline Overview

The pipeline for generating Funscript files is as follows:

1. **YOLO Object Detection**: A YOLO model detects relevant objects (e.g., penis, hands, mouth, etc.) in each frame of the video. The detection results are saved to a `.json` file.
2. **Tracking Algorithm**: A custom tracking algorithm processes the YOLO detection results to track the positions of objects over time. The algorithm calculates distances and interactions between objects to determine the Funscript position.
3. **Funscript Generation**: The tracked data is used to generate a raw Funscript file.
4. **Simplifier**: The raw Funscript data is simplified to remove noise and smooth out the motion. The final `.funscript` file is saved.
5. **Heatmap Generation**: A heatmap is generated to visualize the Funscript data.

---

## Prerequisites
 
Before using this project, ensure you have the following installed:

- **Python 3.8 or higher (tested on 3.11 https://www.python.org/downloads/release/python-3118/)**
- **FFmpeg** added to your PATH or specified under the settings menu (https://www.ffmpeg.org/download.html)
--

## Installation

### Clone the repository
   ```bash
   git clone https://github.com/ack00gar/VR-Funscript-AI-Generator.git
   cd VR-Funscript-AI-Generator
   ```
### Install dependencies
* Install miniconda (https://docs.anaconda.com/miniconda/install/) (We removed venv as all the bat files use conda)
* Start a miniconda command prompt
   
**If your GPU supports CUDA (NVIDIA)**
```bash
conda create -n VRFunAIGen python=3.11
conda activate VRFunAIGen
pip install -r requirements.txt
pip uninstall torch torchvision torchaudio
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
python FSGenerator.py
```
While executing, you’ll need to say “yes” a few times. The lines “pip uninstall / pip3 install” is to replace the “CPU” version of torch with a “cuda enabled / GPU” version (you might need to install nvidia CUDA stuff for it to works, I’m not sure).

**If your GPU doesn't support cuda**
```bash
conda create -n VRFunAIGen python=3.11
conda activate VRFunAIGen
pip install -r requirements.txt
python FSGenerator.py
```

### Download the YOLO model
- Place your YOLO model file (e.g., `k00gar-11n-RGB-200ep-best.mlpackage`) in the `models/` sub-directory.
- Alternatively, you can specify a custom path to the model using the `--yolo_model` argument.


**(Optional) Settings**
Find the settings menu in the app to configure optional option.

### Start script
You can use Start windows.bat to launch the gui on windows if you installed with conda

---

## Command Line Usage

To generate a single script with cmd or terminal, run the following command

```bash
python -m script_generator.cli.generate_funscript_single /path/to/video.mp4
```
See examples/windows/Process single video.bat for an example

To generate scripts for all files in a folder use
```bash
python -m script_generator.cli.generate_funscript_folder /path/to/folder
```
See examples/windows/Process folder.bat for an example

### Command-Line Arguments (Shared)
#### Required Arguments
- **`video_path`** Path to the input video file.  

#### Optional Arguments
- **`--reuse-yolo`** Re-use an existing raw YOLO output file instead of generating a new one when available.
- **`--copy-funscript`** Copies the final funscript to the movie directory.
- **`--save-debug-file`** Saves a debug file to disk with all collected metrics. Also allows you to re-use tracking data.

#### Optional Funscript Tweaking Settings
- **`--boost-enabled`** Enable boosting to adjust the motion range dynamically.
- **`--boost-up-percent`** Increase the peaks by a specified percentage to enhance upper motion limits.
- **`--boost-down-percent`** Reduce the lower peaks by a specified percentage to limit downward motion.
- **`--threshold-enabled`** Enable thresholding to control motion mapping within specified bounds.
- **`--threshold-low`** Values below this threshold are mapped to 0, limiting lower boundary motion.
- **`--threshold-high`** Values above this threshold are mapped to 100, limiting upper boundary motion.
- **`--vw-simplification-enabled`** Simplify the generated script to reduce the number of points, making it user-friendly.
- **`--vw-factor`** Determines the degree of simplification. Higher values lead to fewer points.
- **`--rounding`** Set the rounding factor for script values to adjust precision.


### Command-Line Arguments (Folder mode)
- **`--replace-outdated`** Will regenerate outdated funscripts.
- **`--replace-up-to-date`** Will regenerate funscripts that are up to date and made by this app too.
- **`--num-workers`** Number of subprocesses to run in parallel. If you have beefy hardware 4 seems to be the sweet spot but technically your VRAM is the limit.
---

## Performance & Parallel Processing
Our pipeline's current bottleneck lies in the Python code within YOLO.track (the object detection library we use), which is challenging to parallelize effectively in a single process.

However, when you have high-performance hardware you can use the command line (see above) to processes multiple videos simultaneously. Alternatively you can launch multiple instances of the GUI.

We tested speeds of about 60 to 110 fps for 8k 8bit vr videos when running a single process. Which translates to faster then realtime processing already. However, running in parallel mode we tested 
speeds of about 160 to 190 frames per second (for object detection). Meaning processing times of about 20 to 30 minutes for 8bit 8k VR videos for the complete process. More then twice the speed of realtime!

Keep in mind your results may vary as this is very dependent on your hardware. Cuda capable cards will have an advantage here. However, since the pipeline is largely CPU and video decode bottlenecked 
a top of the line card like the 4090 is not required to get similar results. Having enough VRAM to run 3-6 processes, paired with a good CPU, will speed things up considerably though. 

**Important considerations:**
- Each instance requires the YOLO model to load which means you'll need to keep checks on your VRAM to see how many you can load.
- The optimal number of instances depends on a combination of factors, including your CPU, GPU, RAM, and system configuration. So experiment with different setups to find the ideal configuration for your hardware! 😊

---

## Miscellaneous

- For VR only **Fisheye** and **Equirectangular** 180° videos are supported
- 2D POV videos have limited support
- 2D / VR is automatically detected for fisheye/equirectangular detection make sure you keep the file format information in the filename (_FISHEYE190, _MKX200, _LR_180, etc.) 

### Configuration / User settings

See config.py for customizations and user settings (will be replaced with a yaml soon).


---

## Output Files

The script generates the following files in the output directory of you project folder:

1. `_rawyolo.msgpack`: Raw YOLO detection data. Can be re-used when re-generating scripts 
2. `_cuts.msgpack`: Detected scene changes.
3. `_rawfunscript.json`: Raw Funscript data. Can be re-used when re-generating script with different settings.
4. `.funscript`: Final Funscript file.
5. `_heatmap.png`: Heatmap visualization of the Funscript data.
6. `_comparefunscripts.png`: Comparison visualization between the generated Funscript and the reference Funscript (if provided).
7. `_adjusted.funscript`: Funscript file with adjusted amplitude.
8. `_metrics.msgpack`: Contains all the raw metrics collected and can be used to debug your video when processing is completed.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the **Non-Commercial License**. You are free to use the software for personal, non-commercial purposes only. Commercial use, redistribution, or modification for commercial purposes is strictly prohibited without explicit permission from the copyright holder.

This project is not intended for commercial use, nor for generating and distributing in a commercial environment.

For commercial use, please contact me.

See the [LICENSE](LICENSE) file for full details.

---

## Acknowledgments

- **YOLO**: Thanks to the Ultralytics team for the YOLO implementation.
- **FFmpeg**: For video processing capabilities.
- **Eroscripts Community**: For the inspiration and use cases.

---

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

Join the **Discord community** for discussions and support:  
[Discord Community](https://discord.gg/WYkjMbtCZA)

---
