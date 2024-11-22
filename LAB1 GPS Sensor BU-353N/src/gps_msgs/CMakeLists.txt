cmake_minimum_required(VERSION 3.5)
project(gps_msgs)
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/GPSmsg.msg"
  DEPENDENCIES std_msgs
)

include_directories(include)
ament_package()

install(DIRECTORY msg
  DESTINATION share/${PROJECT_NAME}/msg
)
