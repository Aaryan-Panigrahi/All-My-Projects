#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def sub1_callback(msg):
    print(msg.data)
    

if __name__ == '__main__' :
    rospy.init_node("common_sub_node")
    rospy.loginfo("\n\nWelcome to your Chat display\n")

    sub1 = rospy.Subscriber("/topic_chat2", String, sub1_callback)
    
    rospy.spin()



