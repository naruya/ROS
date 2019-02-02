#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "topic_publisher_cpp");

  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<std_msgs::String>("counter", 1000);

  ros::Rate loop_rate(2);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::String msg;

    std::stringstream ss;
    ss << count;
    msg.data = ss.str();

    ROS_INFO("%s", msg.data.c_str());

    pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}
