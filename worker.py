# worker.py (Run this on any worker PC)

import socket
import numpy as np
import io
from skimage.restoration import denoise_nl_means
import time
import sys

# --- Configuration ---
HOST = '10.26.14.233'     # Must be the SERVER's actual IP address
PORT = 65432
# ---------------------

# Denoiser Parameters (Must be the same in server.py)
PATCH_SIZE = 7
PATCH_DISTANCE = 11

def get_denoising_params():
    """Returns the common NLM parameters."""
    return PATCH_SIZE, PATCH_DISTANCE

def run_worker():
    print("WORKER: Starting...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"WORKER: Connected to server at {HOST}:{PORT}")
            
            # 1. Receive image chunk size
            # (Note: Using sys.maxsize to prevent indefinite blocking in simulation)
            s.settimeout(30.0) 
            
            size_bytes = s.recv(4)
            if not size_bytes:
                print("WORKER: Failed to receive chunk size. Server might have timed out waiting for workers.")
                return
            
            chunk_size = int.from_bytes(size_bytes, 'big')
            
            # 2. Receive the image chunk data
            chunk_data = b''
            while len(chunk_data) < chunk_size:
                packet = s.recv(4096)
                if not packet:
                    break
                chunk_data += packet
            
            if len(chunk_data) != chunk_size:
                print("WORKER: Received incomplete data.")
                return
                
            # 3. Deserialize the data
            sigma_bytes = chunk_data[:8]
            array_bytes = chunk_data[8:]
            
            local_sigma = np.frombuffer(sigma_bytes, dtype=np.float64)[0]
            
            buffer = io.BytesIO(array_bytes)
            chunk_array = np.load(buffer)
            
            print(f"WORKER: Received chunk of shape {chunk_array.shape}. Starting denoising...")
            
            # 4. Perform the SLOW Denoising Task
            start_time = time.time()
            
            denoised_array = denoise_nl_means(
                chunk_array,
                h=1.15 * local_sigma,
                patch_size=get_denoising_params()[0],
                patch_distance=get_denoising_params()[1],
                fast_mode=False,
                channel_axis=-1
            )
            
            end_time = time.time()
            print(f"WORKER: Denoising complete. Time: {end_time - start_time:.2f} seconds.")
            
            # 5. Serialize the result
            result_buffer = io.BytesIO()
            np.save(result_buffer, denoised_array) 
            result_data = result_buffer.getvalue()
            
            # 6. Send the result size and data
            result_size_bytes = len(result_data).to_bytes(4, 'big')
            s.sendall(result_size_bytes)
            s.sendall(result_data)
            
    except socket.timeout:
        print("WORKER: Connection timed out while waiting for data.")
    except ConnectionRefusedError:
        print(f"WORKER: ERROR - Connection refused. Ensure server.py is running on {HOST}:{PORT}")
    except Exception as e:
        print(f"WORKER: An error occurred: {e}")
        
    print("WORKER: Exiting.")

if __name__ == '__main__':
    run_worker()