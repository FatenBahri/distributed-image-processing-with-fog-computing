from flask import Flask, request
import cv2
import os
import time

app = Flask(__name__)

# Créer des dossiers pour stocker les images si ils n'existent pas
received_dir = "received_images"
processed_dir = "processed_images"

os.makedirs(received_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

@app.route('/process', methods=['POST'])
def process_image():
    start_time = time.time()  # début du chronomètre pour cette image

    # Recevoir l'image
    file = request.files['image']
    filename = file.filename

    # Sauvegarder l'image reçue dans le dossier "received_images"
    received_path = os.path.join(received_dir, filename)
    file.save(received_path)
    
    # Traitement : conversion en niveaux de gris
    img = cv2.imread(received_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Sauvegarder l'image traitée dans le dossier "processed_images"
    output_filename = "processed_" + filename
    output_path = os.path.join(processed_dir, output_filename)
    cv2.imwrite(output_path, gray)

    end_time = time.time()  # fin du chronomètre
    elapsed = end_time - start_time

    # Retourner le nom du fichier et le temps de traitement
    return f"{output_filename} (temps de traitement : {elapsed:.2f} secondes)"

if __name__ == '__main__':
    import sys
    port = 5000  # port par défaut
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
