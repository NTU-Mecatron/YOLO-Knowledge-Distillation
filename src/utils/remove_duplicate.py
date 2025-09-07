import os
import shutil
import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

def load_and_preprocess_images(image_folder, transform):
    images = []
    file_paths = []
    for file_name in os.listdir(image_folder):
        file_path = os.path.join(image_folder, file_name)
        if file_name.endswith((".png", ".jpg", ".jpeg")):  # Only process image files
            image = Image.open(file_path).convert("RGB")
            image = transform(image)
            images.append(image)
            file_paths.append(file_path)
    return torch.stack(images), file_paths

def remove_duplicates(image_folder, output_folder, threshold=0.98, batch_size=15):
    # Define the pre-trained model for feature extraction
    model = models.resnet50(pretrained=True)
    model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove the classification head
    model.eval()

    # Define preprocessing transforms
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # ImageNet normalization
        ]
    )

    images, file_paths = load_and_preprocess_images(image_folder, transform)

    # Extract embeddings in batches
    embeddings = []

    for i in range(0, len(images), batch_size):
        batch = images[i : i + batch_size]
        with torch.no_grad():
            batch_embeddings = model(batch).squeeze(-1).squeeze(-1)
        embeddings.append(batch_embeddings)

    embeddings = torch.cat(embeddings).numpy()  # Combine all embeddings

    # Compute cosine similarity using matrix dot product
    dot_product = np.dot(embeddings, embeddings.T)
    norms = np.linalg.norm(embeddings, axis=1)
    norm_matrix = np.outer(norms, norms)

    # Avoid division by zero
    norm_matrix[norm_matrix == 0] = 1e-10

    similarity_matrix = dot_product / norm_matrix

    # Identify duplicates
    unique_files = set()  # Track unique files
    duplicates = set()  # Track duplicates

    for i in range(len(file_paths)):
        if file_paths[i] in duplicates:
            continue  # Skip already identified duplicates
        unique_files.add(file_paths[i])  # Add the first occurrence as unique
        for j in range(i + 1, len(file_paths)):
            if similarity_matrix[i, j] >= threshold:
                duplicates.add(file_paths[j])  # Mark duplicates for removal

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Copy unique images to the output folder
    for unique_file in unique_files:
        shutil.copy(unique_file, os.path.join(output_folder, os.path.basename(unique_file)))

    print(f"Duplicate removal complete! Unique images saved to: {output_folder}")