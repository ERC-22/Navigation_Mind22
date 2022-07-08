#!/usr/bin/env python3

import rospy
import actionlib
import roslib
import sys
import rospkg
import csv
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Empty

output_file_path = rospkg.RosPack().get_path('mind_waypoints')+"/saved_path/waypoints.csv"

# Callbacks definition
def active_cb(extra):
	rospy.loginfo("Goal pose being processed")
def feedback_cb(feedback):
	rospy.loginfo("To cancel the goal: 'rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'")
	rospy.loginfo("Current location: "+str(feedback))
def done_cb(status, result):
	if status == 3:
		rospy.loginfo("Goal reached")
		
		rospy.loginfo("Probe deployed on target!")
	if status == 2 or status == 8:
		rospy.loginfo("Goal cancelled")
	if status == 4:
		rospy.loginfo("Goal aborted")

rospy.init_node('send_goal')

navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
navclient.wait_for_server()

# Example of navigation goal
goal = MoveBaseGoal()

args = rospy.myargv(argv=sys.argv)
if len(args) != 2:
	print("ERROR no targer name provided, please edit waypoints.csv file")
	sys.exit(1)

with open(output_file_path, 'r') as file:
	reader = csv.reader(file, delimiter = ',')
	for row in reader:
		#print (row)
		if(row[0] == args[1]):
			goal.target_pose.header.frame_id = "map"
			goal.target_pose.header.stamp = rospy.Time.now()
			goal.target_pose.pose.position.x = float(row[1])
			goal.target_pose.pose.position.y = float(row[2])
			goal.target_pose.pose.position.z = 0.0
			goal.target_pose.pose.orientation.x = 0.0
			goal.target_pose.pose.orientation.y = 0.0
			goal.target_pose.pose.orientation.z = 0.662
			goal.target_pose.pose.orientation.w = 0.750
			navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
			finished = navclient.wait_for_result()




if not finished:
	rospy.logerr("Action server not available!")
else:
	rospy.loginfo ( navclient.get_result())
	pub = rospy.Publisher('/probe_deployment_unit/drop', Empty, queue_size=1)
	my_empty_msg = Empty()
	rospy.sleep(1.0)
	pub.publish(my_empty_msg)
	
