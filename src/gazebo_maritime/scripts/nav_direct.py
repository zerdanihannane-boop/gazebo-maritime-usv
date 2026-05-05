import subprocess
import time

def send_thrust(left, right):
    # Tes commandes exactes qui marchent
    cmd_l = f"gz topic -t /model/wam-V/joint/left_engine_propeller_joint/cmd_thrust -m gz.msgs.Double -p 'data: {left}'"
    cmd_r = f"gz topic -t /model/wam-V/joint/right_engine_propeller_joint/cmd_thrust -m gz.msgs.Double -p 'data: {right}'"
    subprocess.run(cmd_l, shell=True)
    subprocess.run(cmd_r, shell=True)

def set_angle(angle):
    # Tes commandes d'angle
    cmd_l = f"gz topic -t /wamv/left/thruster/joint/cmd_pos -m gz.msgs.Double -p 'data: {angle}'"
    cmd_r = f"gz topic -t /wamv/right/thruster/joint/cmd_pos -m gz.msgs.Double -p 'data: {angle}'"
    subprocess.run(cmd_l, shell=True)
    subprocess.run(cmd_r, shell=True)

print("--- DEPART DU BATEAU ---")
# 1. On s'assure que les moteurs sont droits
set_angle(0.0)
time.sleep(1)

# 2. On avance pendant 10 secondes (Point A vers Point B)
print("Avancement vers le point B...")
send_thrust(300.0, 300.0)
time.sleep(10) 

# 3. Arrivé au point B : On coupe tout et on redresse
print("Arrivé ! Arrêt des moteurs et redressement.")

# On coupe la puissance d'abord
send_thrust(0.0, 0.0)

# ON RAJOUTE ÇA ICI : On remet les moteurs à 0 pour éviter qu'il pivote
set_angle(0.0)

print("Bateau stabilisé.")
