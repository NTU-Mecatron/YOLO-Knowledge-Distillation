from ultralytics import YOLO 

teacher_model = "teacher.pt"
student_name = "training_and_test/student_models/any_name_you_want" #change the file name after student_models to the actual name of the folder you want the model + result to be in

def train_student(teacher_model, input_data_path):
    model = YOLO(teacher_model)
    results = model.train(data = input_data_path,
                      epochs = 100, imgsz = 640, batch = 16, workers = 6, patience = 100, cache = False, close_mosaic = 10, device='0', project = student_name, freeze = 15, lr0 = 0.005)

if __name__ == '__main__':
    final_model_path = "path_to_final_data_that_you_downloaded_from_roboflow"
    train_student(teacher_model, final_model_path) #change the path to the final data folder 