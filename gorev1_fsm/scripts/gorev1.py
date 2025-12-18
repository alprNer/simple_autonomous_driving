#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import math

class Gorev1FSM:
    def __init__(self):
        rospy.loginfo("Gorev 1 baslatildi.")

        self.cmd_vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        self.state_pub = rospy.Publisher('~state', String, queue_size=1)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.state = "ILERI"

        
        self.forward_speed = 0.15  
        self.turn_speed = 0.45

        
        self.obstacle_dist = 1.0      
        self.side_safe_dist = 0.5     
        self.critical_dist = 0.7      

        
        self.blind_spot_side = 0.20   
        self.blind_spot_front = 0.15  

        self.min_front_dist = float('inf')
        self.min_left_dist = float('inf')
        self.min_right_dist = float('inf')

        rospy.Timer(rospy.Duration(0.1), self.control_loop)

    def scan_callback(self, msg):
        ranges = msg.ranges
        total = len(ranges)

        
        front_width = int(total * 0.10)   
        front_ranges = ranges[0:front_width] + ranges[-front_width:]
        
        
        front = [r for r in front_ranges if not math.isinf(r) and r > self.blind_spot_front]
        self.min_front_dist = min(front) if front else float('inf')

        
        left_start = int(total * 0.20)
        left_end = int(total * 0.30)
        left_ranges = ranges[left_start:left_end]

        
        left = [r for r in left_ranges if not math.isinf(r) and r > self.blind_spot_side]
        self.min_left_dist = min(left) if left else float('inf')

        
        right_start = int(total * 0.70)
        right_end = int(total * 0.80)
        right_ranges = ranges[right_start:right_end]

        
        right = [r for r in right_ranges if not math.isinf(r) and r > self.blind_spot_side]
        self.min_right_dist = min(right) if right else float('inf')

        # FSM

        
        if self.min_front_dist < self.critical_dist:
            self.state = "KACIN"

        
        elif self.state == "ILERI" and (
            self.min_front_dist < self.obstacle_dist or 
            self.min_left_dist < self.side_safe_dist or 
            self.min_right_dist < self.side_safe_dist
        ):
            rospy.loginfo("ENGEL: On:%.2f Sol:%.2f Sag:%.2f -> DONUS", 
                          self.min_front_dist, self.min_left_dist, self.min_right_dist)
            self.state = "DONUS"

        
        elif self.state in ["DONUS", "KACIN"] and (
            self.min_front_dist > (self.obstacle_dist + 0.2) and
            self.min_left_dist > self.side_safe_dist and
            self.min_right_dist > self.side_safe_dist
        ):
            rospy.loginfo("YOL ACIK -> ILERI")
            self.state = "ILERI"
        
        self.state_pub.publish(self.state)

    def control_loop(self, event):
        t = Twist()

        if self.state == "ILERI":
            t.linear.x = self.forward_speed
            t.angular.z = 0.0

        elif self.state == "DONUS":
            t.linear.x = 0.0
            t.angular.z = self.turn_speed

        elif self.state == "KACIN":
            t.linear.x = -0.10 
            t.angular.z = self.turn_speed

        self.cmd_vel_pub.publish(t)

if __name__ == "__main__":
    rospy.init_node("gorev1_fsm_node")
    try:
        Gorev1FSM()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
