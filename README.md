# Distributed Image Processing with Fog Computing

## Description

Ce mini-projet illustre un système de traitement d’images distribué utilisant le concept de Fog Computing.  
Le Master Node distribue des images à plusieurs Worker Nodes qui les traitent en parallèle et renvoient le résultat.
--> Le **Master Node (Fog Node)** tourne sur **Windows** et distribue les images à plusieurs **Worker Nodes (nœuds simples)** qui tournent sur **WSL**.  
Chaque Worker Node s’exécute sur un **port différent**, reçoit des images, les traite en parallèle (conversion en niveaux de gris) et renvoie le résultat.  -->chque worker run sur un terminal different
---> Cette architecture permet de simuler le traitement distribué et le parallélisme, même sur un seul PC, tout en respectant le principe du Fog Computing.


## Structure du projet

distributed-image-processing-fog/
│
├─ README.md
├─ images/                # Images originales
├─ master_node.py
│   
├─ worker1/
│   ├─worker_node.py
|   ├─received_images/
|   ├─processed_images/
├─ worker2/
│   ├─worker_node.py
|   ├─received_images/
|   ├─processed_images/
├─ worker3/
│   ├─worker_node.py
|   ├─received_images/
|   ├─processed_images/


## Prérequis

- Python 3.x
- Modules Python : `opencv-python-headless`, `flask`, `requests`

