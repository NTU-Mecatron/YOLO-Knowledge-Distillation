# YOLO Knowledge Distillation Pipeline (DEPRECATED)

> [!WARNING]
> **This repository is deprecated and no longer maintained.**
> The knowledge-distillation pipeline now lives in
> [NTU-Mecatron/perception_training](https://github.com/NTU-Mecatron/perception_training),
> together with the rest of the perception tooling. Please use that repo for new work
> and open issues/PRs there.
>
> | Here | In perception_training |
> |---|---|
> | `python src/extract_frames.py --source ...` | `video2frames --source ...` |
> | `python src/label_data.py --teacher_model ...` | `auto-label --teacher-model ...` |
> | `python src/upload_to_rf.py --api_key ...` | `roboflow-upload --project-id ... --batch-name ...` |
> | `python src/augment_imgs.py` | `augment-images` |
> | `python src/train.py` (edit params in code) | `pt-train --config configs/train/kd_student.yaml` |
>
> See the *Knowledge distillation pipeline* section of the
> [perception_training README](https://github.com/NTU-Mecatron/perception_training#knowledge-distillation-pipeline).
Package for autolabelling images using a pre-trained YOLO model and upload the labelled data to Roboflow. This is so that we do not have to use Roboflow credit to label data:>

## Installation

### Windows
For a fresh setup, run the `setup.ps1` script from PowerShell. This will create a Python virtual environment named `kd_venv` and install all the necessary packages from `requirements.txt`.

Before running the script, you may need to set the execution policy to allow scripts to run. You can do this by running the following command in PowerShell as an administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
Then, run the setup script:
```powershell
.\setup.ps1
```
Activate the virtual environment
```powershell
.\kd_venv\Scripts\Activate.ps1
```

### Linux
For Linux, use the `setup.sh` script. First, make the script executable:
```bash
chmod +x setup.sh
```
Then, run the script:
```bash
./setup.sh
```
Activate virtual environment
```bash
source kd_venv/bin/activate
```

## Dependencies Setup
Next install the pytorch version that is compatible with your GPU CUDA version. You can check this by running 
```bash
nvidia-smi 
```
After that, run this pip install script to install the pytorch version that is appropriate for your cuda version.
For more info, visit https://pytorch.org/get-started/locally/
For example, if my GPU is running in CUDA 12.8:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```
If your GPU is not CUDA compatible, run
```bash
pip install torch torchvision 
```
After that, run 
```bash
pip install -r requirements.txt
```
   
## Usage

0. Use VLC media player to convert to standard encoding. (Compulsory step) It has been found that videos with non standard encoding will produce different results for removing blurry images, and even for training. 

> Open VLC media player, go to Media > Convert/Save. Add the video file you want to convert, then click on Convert/Save. In the Convert window, choose a profile `Video - H.264 + MP3 (MP4)` and specify a destination file (use the original filename and add "-converted"). Click Start to begin the conversion process.

1. Extract, resize and remove blurry images:
```bash
python src/extract_frames.py --source path/to/video --fps 2
```

2. Label data using a pre-trained YOLO model:
```bash
python src/label_data.py --teacher_model yolo_models/your_model.pt --conf 0.25 --iou 0.7
```

3. Upload images and labels to Roboflow:
```bash
python src/upload_to_rf.py --api_key your_api_key --project_id your_project_id --batch_name set_a_batch_name
```

4. Perform augmentations, dataset split and export dataset in Roboflow.

5. Train (you may need to change the parameters in `src/train.py`):
```bash
python src/train.py