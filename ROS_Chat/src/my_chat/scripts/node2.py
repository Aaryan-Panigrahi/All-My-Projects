#!/usr/bin/env python3

import rospy
import threading
from std_msgs.msg import String

#PSEUDO-CODE 
# Basically the same as node1.py
# Different node-name, same topic-name!


def publisher():
    while not rospy.is_shutdown():
        msg = input()
        pub2.publish('\t\t\t' + usr + '\t' + msg)
        #pub2.publish(usr + '\t' + msg + '\n')

def subscriber():
    sub2 = rospy.Subscriber("/topic_chat", String, sub2_callback)
    rospy.spin()
    
def sub2_callback(msg):
    if usr not in msg.data:
        print(msg.data)
        print(usr)


if __name__ == '__main__' :

    rospy.init_node("node2")
    rospy.loginfo("Hello, 2nd user node initiated!")

    usr = input('Hi. Please enter your username : ') + ' :  '

    print('\n' + usr)

    pub2 = rospy.Publisher("/topic_chat", String, queue_size=10 )

    t1 = threading.Thread(target=publisher)
    t2 = threading.Thread(target=subscriber)

    t1.start()
    t2.start()


