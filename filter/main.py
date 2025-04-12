import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import faiss
from PIL import Image
import os

# Initialization of the BLIP-2 model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


def extract_image_features(image):
    """Extracts image features as an embedding vector."""
    # Convert image to RGB format (if not already in this format)
    image = image.convert('RGB')

    # Resize the image to 224x224 (required size for the BLIP model)
    image = image.resize((224, 224))

    # Process the image using the BLIP processor
    inputs = processor(images=image, return_tensors="pt")

    # Extract features using the BLIP model
    with torch.no_grad():
        features = model.vision_model(inputs.pixel_values)[1]  # Retrieve visual embeddings

    # Convert features to numpy format and return
    return features.numpy().astype('float32')


# Initialization of global variables
index = None  # FAISS index will be initialized dynamically
image_embeddings = []
image_labels = []


# Function to add multiple images to the database
def add_images_to_database(images_path):
    global index, image_embeddings, image_labels
    results = []

    for image in os.listdir(images_path):
        # Open the image using PIL
        img = Image.open(images_path + image)

        # Extract image features
        embed = extract_image_features(img)

        # If FAISS index has not been created yet, initialize it with the correct dimension
        if index is None:
            embedding_dim = embed.shape[1]  # Get embedding dimension from the first image
            index = faiss.IndexFlatL2(embedding_dim)  # Initialize FAISS index

        # Add embeddings and labels to the database
        image_embeddings.append(embed)
        image_labels.append(image)
        index.add(embed)

        results.append(f"Added image: {image}")

    return "\n".join(results)


# Function to search FAISS based on a new image
def find_closest_image(query_image):
    query_embed = extract_image_features(query_image)
    D, I = index.search(query_embed, 1)  # Retrieve the closest neighbor

    closest_index = I[0][0]
    distance = D[0][0]


    if closest_index < len(image_labels):
        return f"Closest image: {image_labels[closest_index]} (Similarity: {distance})"
    else:
        return "No matching image found."
CLASSES_PATH = 'classes/'
IMG_PATH = 'test3.png'
img = Image.open(IMG_PATH)

print(add_images_to_database(CLASSES_PATH))
print(find_closest_image(img))