import requests
import os
import time # pour mesurer le temps
# Liste des nœuds simples (IP + port)
simple_nodes = [
  "http://172.25.45.246:5000/process",  # IP de la  worker 1 sous Linux wsl
    "http://172.25.45.246:5002/process",  # IP de la  worker 2 sous Linux wsl
    #"http://172.25.45.246:5003/process"  # IP de la  worker 3 sous Linux wsl
   # "http://10.26.14.233:5000/process" ,
    #"http://10.26.14.116:5000/process" ,
    #"http://10.26.13.73:5000/process" 




]

# Dossier contenant les images à traiter
node_times = {node: 0.0 for node in simple_nodes}
image_folder = "images"
images = [os.path.join(image_folder, img) for img in os.listdir(image_folder)
          if img.endswith((".jpg", ".png", ".jpeg"))]
start_time = time.time() # début chronomètre global

# Distribution des images aux nœuds simples
for idx, img_path in enumerate(images):
    node = simple_nodes[idx % len(simple_nodes)]  # répartition équitable
    with open(img_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(node, files=files)
        print(f"Image envoyée à {node} → résultat : {response.text}")
end_time = time.time() # fin chronomètre global
total_time = end_time - start_time

print("Toutes les images ont été distribuées et traitées !")
print(f"Temps total d'exécution : {total_time:.2f} secondes")