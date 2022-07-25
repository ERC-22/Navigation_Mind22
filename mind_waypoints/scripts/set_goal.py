#!/usr/bin/env python3

import rospy
import actionlib
import roslib
import sys
import rospkg
import csv
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Empty

# Load the waypoints file
output_file_path = rospkg.RosPack().get_path('mind_waypoints')+"/saved_path/waypoints.csv"
# Waypoints ordered list

# Take target from user terminal inputs in order
#args = rospy.myargv(argv=sys.argv)
#if len(args) != 2:
#	rospy.loginfo("ERROR no target name provided, please edit waypoints.csv file")
#	sys.exit(1)
# populate waypoints
#for i in range(len(args)):
#	if(i != 0):
#		waypoints.append(args[i])

# Callbacks definition
def active_cb(extra):
	rospy.loginfo("Goal pose being processed")
def feedback_cb(feedback):
	rospy.loginfo("To cancel the goal: 'rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'")
	rospy.loginfo("Current location: "+str(feedback))
def done_cb(status, result):
	if status == 3:
		rospy.loginfo("Goal reached")
		# Probe deployment
		if (probe == True):
			pub = rospy.Publisher('/probe_deployment_unit/drop', Empty, queue_size=1)
			my_empty_msg = Empty()
			rospy.sleep(1.0)
			pub.publish(my_empty_msg)
			rospy.loginfo("Probe deployed on target!")
	if status == 2 or status == 8:
		rospy.loginfo("Goal cancelled")
	if status == 4:
		rospy.loginfo("Goal aborted")

def caller(target):
	rospy.loginfo(waypoints)
	navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	navclient.wait_for_server()
	# Example of navigation goal
	goal = MoveBaseGoal()
	# Read the .csv file
	with open(output_file_path, 'r') as file:
		reader = csv.reader(file, delimiter = ',')
		for row in reader:
			#print (row)
			if(row[0] == target):
				goal.target_pose.header.frame_id = "map"
				goal.target_pose.header.stamp = rospy.Time.now()
				goal.target_pose.pose.position.x = float(row[1])
				goal.target_pose.pose.position.y = float(row[2])
				goal.target_pose.pose.position.z = 0.0
				goal.target_pose.pose.orientation.x = 0.0
				goal.target_pose.pose.orientation.y = 0.0
				#goal.target_pose.pose.orientation.z = 0.662
				#goal.target_pose.pose.orientation.w = 0.750
				goal.target_pose.pose.orientation.z = 0.0
				goal.target_pose.pose.orientation.w = 1.0
				rospy.loginfo("Your goal is being sent!\n")
				navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
				finished = navclient.wait_for_result()
				
############################################################################################
				if not finished:
					rospy.logerr("Action server not available!")
				else:
					rospy.loginfo ( navclient.get_result())
	
def controller():
		# init the node
		rospy.init_node('send_goal')
		print('######################################')
		print('##### Mind Cloud Pilot Interface #####')
		print('######################################\n')
		print('Please make sure your .csv file is properly set!\n\n')
		print('1: send waypoints sequence (point by point)\n')
		print('2: refresh .csv and navigate\n')
		print('3: get back to initial position\n')
		print('4: Shutdown program\n')
		global waypoints
		global probe
		inp = input()
		if inp =='1':
			waypoints=[]
			rospy.loginfo('Enter number of waypoints\n')
			rospy.loginfo(waypoints)
			no_of_pts= input()
			rospy.loginfo('Enter your points names\n')
			for i in range(int(no_of_pts)):
				something=input()
				waypoints.append(something)
				print(waypoints)
			for target in waypoints:
				if(len(target)==1):
					probe = True
				else:
					probe = False
				caller(target)
			controller()
		elif inp =='2':
			waypoints=[]
			with open(output_file_path, 'r') as file:
				reader = csv.reader(file, delimiter = ',')
				for row in reader:
					if(row[0]=='point'):
						pass
					else:
						waypoints.append(row[0])
			for target in waypoints:
				if(len(target)==1):
					probe = True
				else:
					probe = False
				caller(target)
				rospy.sleep(0.5)
			controller()
			
		elif inp =='3':
			waypoints=[]
			waypoints.append('h')
			for target in waypoints:
				caller(target)
			controller()
			
		elif inp =='4':
			sys.exit(1)
		else :
			rospy.loginfo('Please enter a valid option!\n')
			controller()
		
if __name__ == '__main__':
	try:
		controller()
	except rospy.ROSInterruptException:
		pass
