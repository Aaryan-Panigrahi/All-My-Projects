#!/usr/bin/env python3

import rospy
from std_msgs.msg import String


if __name__ == '__main__' :
    rospy.init_node("pub_node1")
    rospy.loginfo("Hello, 1st user node initiated!")
    usr = input('Hi. Please enter your username : ') + ': '

    pub1 = rospy.Publisher("topic_chat2", String, queue_size=10 )
    
    while not rospy.is_shutdown():
        msg = input(usr)
        pub1.publish(usr + '\t' + msg + '\n')



