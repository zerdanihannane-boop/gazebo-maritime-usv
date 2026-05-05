import subprocess
import time
import re
import math

def send_thrust(left, right):
    cmd_l = f"gz topic -t /model/wam-V/joint/left_engine_propeller_joint/cmd_thrust -m gz.msgs.Double -p 'data: {left}'"
    cmd_r = f"gz topic -t /model/wam-V/joint/right_engine_propeller_joint/cmd_thrust -m gz.msgs.Double -p 'data: {right}'"
    subprocess.run(cmd_l, shell=True)
    subprocess.run(cmd_r, shell=True)

def get_real_data():
    cmd = "gz topic -e -t /world/sydney_regatta/pose/info -n 1"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        content = result.stdout.split("name: \"wam-V\"")[1]
        x = float(re.findall(r"x: ([-+]?\d*\.\d+|\d+)", content)[0])
        z_rot = float(re.findall(r"z: ([-+]?\d*\.\d+|\d+)", content)[1]) 
        return x, z_rot
    except:
        return None, None

# --- PARAMÈTRES DU SMC ---
lambda_s = 0.8   # Pente de la surface de glissement
K_reach = 60.0  # Gain de robustesse (équivalent à la force de réaction)
poussee_base = 80.0
start_x = -532.0
target_distance = 140.0
target_x = start_x + target_distance

prev_error = 0
print("--- DÉMARRAGE COMMANDE SMC (MODE GLISSANT) ---")

while True:
    x, rot = get_real_data()
    if x is None: continue

    distance_parcourue = x - start_x
    
    # 1. Calcul de l'erreur d'angle et de sa dérivée
    error = 0.0 - rot
    dot_error = error - prev_error # Variation de l'erreur
    
    # 2. SURFACE DE GLISSEMENT (S)
    # C'est la ligne droite vers laquelle on veut forcer le système
    S = dot_error + lambda_s * error
    
    # 3. LOI DE COMMANDE SMC
    # On utilise 'tanh' pour adoucir le passage de la surface et éviter les vibrations
    correction = K_reach * math.tanh(S)
    
    # Application sur les moteurs
    t_left = poussee_base - correction
    t_right = poussee_base + correction

    # Bornes de sécurité
    t_left = max(min(t_left, 250.0), -250.0)
    t_right = max(min(t_right, 250.0), -250.0)

    # Condition d'arrêt
    if distance_parcourue >= target_distance:
        send_thrust(-100.0, -100.0) # Frein
        time.sleep(0.4)
        break

    print(f"SMC | Dist: {distance_parcourue:.1f}m | S: {S:.3f} | Correction: {correction:.2f}")
    
    send_thrust(t_left, t_right)
    prev_error = error
    time.sleep(0.1)

send_thrust(0.0, 0.0)
print("Arrivée SMC terminée.")
