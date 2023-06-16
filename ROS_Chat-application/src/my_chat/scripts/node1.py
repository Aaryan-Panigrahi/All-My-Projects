#!/usr/bin/env python3

import rospy
import threading
from std_msgs.msg import String

#PSEUDO-CODE

    #Thread - 1 (Publisher)
    #while not shutdown
    #   msg = input(usr)
    #   pub1.publish(usr + msg + '\n')

    #Thread - 2 (Subscriber)
    #sub1 = rospy.Subscriber("/topic_chat", String, sub1_callback)
    #rospy.spin (repeat till shutdown)


def publisher():
    while not rospy.is_shutdown():
        msg = input()
        pub1.publish('\t\t\t' + usr + '\t' + msg)
        #pub1.publish(usr + '\t' + msg + '\n')

def subscriber():
    sub1 = rospy.Subscriber("/topic_chat", String, sub1_callback)
    rospy.spin()

  
def sub1_callback(msg):
    if usr not in msg.data:
        print(msg.data)
        print(usr)
    

if __name__ == '__main__' :

    rospy.init_node("node1")
    rospy.loginfo("Hello, 1st user node initiated!")

    usr = input('Hi. Please enter your username : ') + ' : '

    print('\n' + usr)

    pub1 = rospy.Publisher("/topic_chat", String, queue_size=10 )

    pub_thread = threading.Thread(target=publisher)
    sub_thread = threading.Thread(target=subscriber)

    pub_thread.start()
    sub_thread.start()



