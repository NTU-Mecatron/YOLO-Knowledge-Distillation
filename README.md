# Automated-KD-Pipeline
I've only used this in Python 3.12, other versions have not been tested. 

## Virtual Environment Setup
### If you are on Windows:
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

### If you are on Linux:
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
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```
If your GPU is not CUDA compatible, run
```bash
pip3 install torch torchvision 
```
After that, run 
```bash
pip install -r requirements.txt
```
Also, don't forget to get rid of all the fillers in the folders!
   
## DATA PREPARATION PHASE 
The data prepartion phase consists of these following parts: frame extraction, preprocessing, augmentation, and labelling. 
1. Frame extraction extracts the frames of the specified video at a specified target fps (make sure that you specify an integer as the target fps), and resizes the biggest dimension to 640. 
```bash
python -m src.extract_frames --video_path=path/to/video --target_fps=3
```
2. The augmentation part applies various augmentation to the images that are preprocessed. It also splits up the images into train and valid sets for training later and outputs them into a folder called "labelled_data" You can set two parameters when launching this file in the terminal: augmentation multiplier is the resulting multiplier of the original dataset as a result of augmentation processes, and the valid_size is the size of the valid set that you can set (0.2 means 20% valid, 80% train) 
```bash
python -m src.augment_imgs --aug_multiplier=3 --valid_size=0.2
```
3. Finally, the label generation part takes in those augmented images and runs inference on them using a specified teacher yolo_model at a specified confidence threshold, and generates the label data as well as the .yaml file in the labelled_data folder. 
```bash
python -m src.label_data --base_model=/path/to/yolo_model --conf_threshold=0.3 --iou_threshold = 0.6
```

## DATA UPLOADING PHASE
To upload the data to ROBOFLOW, you must first create a project within a ROBOFLOW workspace and obtain the complete project ID and the API key. You can obtain the project ID by selecting the three dots at the top right hand corner of the project and clicking on "copy project ID". You can obtain the API key by going to settings and clicking on "API KEYS". After that, go to the upload_rf.py file and paste it in the project name.
```bash
python -m src.upload_to_rf --api_key=your_api_key --project_id=your_project_id --batch_name=set_a_batch_name
```

### IMPORTANT: Class name change when uploading to RF
for some reason, when I upload annotation files to RF, the spaces in the class names gets convereted to - automatically. For example, label files says "Blue pail" but at roboflow, it appears as "Blue-pail". To fix this, go to the classes and tags part of the project and correct this mistake. 

## DATA TRAINING AND TESTING PHASE
After uploading all the data to roboflow, go through them manually to check if everything is correct. You can then run the student_training.py file in src to train the model through YOLO. Make sure to specify the folder path as well as tweak any settings that you'd like. 
