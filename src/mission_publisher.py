#!/usr/bin/env python

import rospy
import yaml
from geometry_msgs.msg import PoseStamped
import threading


class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)


def mission_publisher(pose_list, robot_name):
    pub = rospy.Publisher(robot_name + '/mission', PoseStamped, queue_size=10, latch=True)
    for pose in pose_list:
        pub.publish(pose)
        rospy.loginfo("{"+robot_name+"} New mission published")
        rospy.sleep(10)

if __name__ == '__main__':
    rospy.init_node("mission_publisher_node", log_level=rospy.INFO)
    mission_file = rospy.get_param('mission_file')
    robot_list = rospy.get_param('robot_list')

    f = open(mission_file)
    missions = yaml.load(f)
    pub_thread = dict()

    rospy.sleep(1)

    for robot in robot_list:
        pub_thread[robot] = FuncThread(mission_publisher, missions[robot], robot)
        pub_thread[robot].start()

    for robot in robot_list:
        pub_thread[robot].join()
