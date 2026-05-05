import subprocess
import time
import re

def send_thrust(left, right):
    cmd_l = f"gz topic -t /model/wam-V/joint/left_engine_propeller_joint/cmd_thrust -m gz.msgs.Double -p 'data: {left}'"
    cmd_r = f"gz topic -t /model/wam-V/joint/right_engine_propeller_joint/cmd_thrust -m gz.msgs.Double -p 'data: {right}'"
    subprocess.run(cmd_l, shell=True)
    subprocess.run(cmd_r, shell=True)

def get_real_data():
    # On récupère la position et on vérifie s'il y a un obstacle via les topics de collision
    cmd = "gz topic -e -t /world/sydney_regatta/pose/info -n 1"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        content = result.stdout.split("name: \"wam-V\"")[1]
        x = float(re.findall(r"x: ([-+]?\d*\.\d+|\d+)", content)[0])
        z_rot = float(re.findall(r"z: ([-+]?\d*\.\d+|\d+)", content)[1]) 
        return x, z_rot
    except:
        return None, None

# --- RÉGLAGES PID ---
Kp = 45.0
Ki = 0.01
Kd = 22.0

# --- PARAMÈTRES DE MISSION ---
start_x = -532.0         # Position de départ typique dans Sydney Regatta
target_distance = 140.0  # On s'arrête à 140m pour ne pas dépasser tes 150m max
target_x = start_x + target_distance 

prev_error = 0
integral = 0
poussee_base = 90.0

print(f"--- MISSION : Point A vers B ({target_distance}m) ---")

while True:
    x, rot = get_real_data()
    if x is None: continue

    # 1. CALCUL DE L'ERREUR DE DIRECTION (Rester droit à 0.0)
    error = 0.0 - rot
    
    # 2. CALCUL PID COMPLET
    integral += error
    derivative = error - prev_error
    correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
    
    # 3. LOGIQUE D'ÉVITEMENT D'OBSTACLE (Simple)
    # Si la correction devient énorme d'un coup, c'est qu'on dévie à cause d'un choc
    if abs(error) > 0.5: 
        print("Obstacle ou déviation détectée ! Manœuvre d'évitement...")
        t_left = -50.0   # On recule un peu à gauche
        t_right = 50.0   # On tourne à droite
    else:
        t_left = poussee_base - correction
        t_right = poussee_base + correction

    # Bornes de sécurité
    t_left = max(min(t_left, 250.0), -250.0)
    t_right = max(min(t_right, 250.0), -250.0)

    # 4. VÉRIFICATION DE LA DISTANCE
    distance_parcourue = x - start_x
    if distance_parcourue >= target_distance:
        print("Objectif atteint (140m) !")
        break

    print(f"Avancement: {distance_parcourue:.1f}m / {target_distance}m | Correction: {correction:.2f}")
    
    send_thrust(t_left, t_right)
    prev_error = error
    time.sleep(0.1)

# ARRÊT
send_thrust(0.0, 0.0)
print("Bateau stoppé au point B.")
