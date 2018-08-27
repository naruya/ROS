#!/usr/bin/env python
# BEGIN ALL
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
  global g_range_ahead
  # print len(msg.ranges) # 360
  g_range_ahead = min(msg.ranges[len(msg.ranges)/2-10:len(msg.ranges)/2+10]) # min(msg.ranges)


g_range_ahead = 1 # anything to start
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rospy.init_node('wander')
state_change_time = rospy.Time.now() + rospy.Duration(5)
driving_forward = False
rate = rospy.Rate(10)

while not rospy.is_shutdown():
  if driving_forward:
    # print "range ahead: %0.1f" % g_range_ahead
    # print g_range_ahead
    # BEGIN FORWARD
    # if (g_range_ahead < 0.3):
    if (g_range_ahead < 0.6 or rospy.Time.now() > state_change_time):
      driving_forward = False
      state_change_time = rospy.Time.now() + rospy.Duration(1)
    # END FORWARD
  else: # we're not driving_forward
    # BEGIN TURNING
    if (g_range_ahead > 0.8 or rospy.Time.now() > state_change_time):
      driving_forward = True # we're done spinning, time to go forwards!
      state_change_time = rospy.Time.now() + rospy.Duration(1)
    # END TURNING
  twist = Twist()
  if driving_forward:
    twist.linear.x = -0.5
    twist.angular.z = 0.
  else:
    twist.linear.x = 0.1
    twist.angular.z = 0.3
  cmd_vel_pub.publish(twist)

  rate.sleep()
# END ALL
