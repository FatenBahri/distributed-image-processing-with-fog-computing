import requests
import os

# Liste des nœuds simples (IP + port)
simple_nodes = [
    "http://172.25.45.246:5000/process",  # IP de la  worker 1 sous Linux wsl
    "http://172.25.45.246:5001/process",  # IP de la  worker 2 sous Linux wsl
    "http://172.25.45.246:5002/process"  # IP de la  worker 3 sous Linux wsl

]

# Dossier contenant les images à traiter
image_folder = "images"
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder)
          if img.endswith((".jpg", ".png", ".jpeg"))]

# Distribution des images aux nœuds simples
for idx, img_path in enumerate(images):
    node = simple_nodes[idx % len(simple_nodes)]  # répartition équitable
    with open(img_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(node, files=files)
        print(f"Image envoyée à {node} → résultat : {response.text}")

print("Toutes les images ont été distribuées et traitées !")
