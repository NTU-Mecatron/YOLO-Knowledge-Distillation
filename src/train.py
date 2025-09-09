from ultralytics import YOLO 

def train_student(teacher_model, input_data):
    model = YOLO(teacher_model)
    model.train(data = input_data,
        epochs = 100, imgsz = 640, batch = 32, workers = 6, cache = True, close_mosaic = 10, device='0')

if __name__ == '__main__':
    teacher_model = "teacher.pt"
    input_data = "path_to_downloaded_yaml_file"
    train_student(teacher_model, input_data)