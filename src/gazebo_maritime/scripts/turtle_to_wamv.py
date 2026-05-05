#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class TurtleBridge(Node):
    def __init__(self):
        super().__init__('turtle_bridge')
        
        # On écoute la tortue
        self.subscription = self.create_subscription(Twist, '/turtle1/cmd_vel', self.listener_callback, 10)
        
        # On parle au bateau
        self.left_pub = self.create_publisher(Float64, '/model/wamv/joint/left_engine_propeller_joint/cmd_thrust', 10)
        self.right_pub = self.create_publisher(Float64, '/model/wamv/joint/right_engine_propeller_joint/cmd_thrust', 10)

    def listener_callback(self, msg):
        # On transforme la vitesse de la tortue en poussée pour le bateau
        vitesse = msg.linear.x * 100.0  # On multiplie par 100 pour avoir de la force
        rotation = msg.angular.z * 50.0
        
        left_thrust = Float64()
        right_thrust = Float64()
        
        # Calcul simple pour tourner (différentiel)
        left_thrust.data = vitesse - rotation
        right_thrust.data = vitesse + rotation
        
        self.left_pub.publish(left_thrust)
        self.right_pub.publish(right_thrust)

def main(args=None):
    rclpy.init(args=args)
    bridge = TurtleBridge()
    rclpy.spin(bridge)
    bridge.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
