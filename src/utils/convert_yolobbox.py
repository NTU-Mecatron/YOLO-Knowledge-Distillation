import os
import yaml

def convert_yolo_folder(yaml_path, label_folder):
    
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        names = data['names']

    def convert_yolo_to_bbox_inplace(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue  # Skip invalid lines

            class_id = names[int(parts[0])]
            if class_id is None:
                print(f"Warning: Class ID {parts[0]} not found in names mapping. Skipping line in {file_path}")
                continue
            x_center, y_center, w, h = map(float, parts[1:])

            # Compute four corner points (MUST USE NORMALIZED COORDS APPARENTLY)
            x_min = x_center - (w / 2)
            y_min= y_center - (h / 2)
            x_max = x_center + (w / 2)
            y_max = y_center + (h / 2)
            converted_lines.append(f"{class_id} {x_min:.6f} {y_min:.6f} {x_max:.6f} {y_max:.6f}\n")

        # Save the converted files by overwriting the original file
        with open(file_path, "w") as f:
            f.writelines(converted_lines)

    # Process each label file
    for txt_file in os.listdir(label_folder):
        if txt_file.endswith(".txt"):
            file_path = os.path.join(label_folder, txt_file)
            convert_yolo_to_bbox_inplace(file_path)
            print(f"Converted in-place: {txt_file}")

