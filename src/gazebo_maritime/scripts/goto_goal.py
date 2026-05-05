#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math

class WAMVNavigator(Node):
    def __init__(self):
        super().__init__('wamv_navigator')
        
        # 1. Configuration des Publishers (Envoi des commandes)
        self.left_pub = self.create_publisher(Float64, '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_pub = self.create_publisher(Float64, '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)
        
        # 2. Point B (Cible) - Tu peux changer ces chiffres !
        self.target_x = 50
        self.target_y = 5.0
        
        # 3. Position actuelle (A) - À terme, cela viendra d'un capteur GPS
        self.curr_x = 0.0
        self.curr_y = 0.0
        
        # Boucle de contrôle (tourne 10 fois par seconde)
        self.timer = self.create_timer(0.1, self.navigate)
        self.get_logger().info('Navigateur WAM-V lancé. En attente de départ...')

    def navigate(self):
        # --- MATHS ---
        # Distance (Pythagore)
        dist = math.sqrt((self.target_x - self.curr_x)**2 + (self.target_y - self.curr_y)**2)
        
        # Angle vers la cible (Atan2)
        # angle_cible = math.atan2(self.target_y - self.curr_y, self.target_x - self.curr_x)

        msg = Float64()
        
        if dist > 1.5:
            self.get_logger().info(f'Distance cible : {dist:.2f} m')
            msg.data = 400.0  # On pousse fort
        else:
            self.get_logger().info('POINT B ATTEINT ! Arrêt des moteurs.')
            msg.data = 0.0
            
        self.left_pub.publish(msg)
        self.right_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    navigator = WAMVNavigator()
    try:
        rclpy.spin(navigator)
    except KeyboardInterrupt:
        pass
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
