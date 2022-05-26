cmake_minimum_required(VERSION 2.8.3)
project(leo_navigation)

#find_package(catkin)
find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  message_filters
  roscpp
  pcl_conversions
  pcl_ros
  sensor_msgs
  tf2_ros
  tf2_geometry_msgs
  tf2_sensor_msgs
)

catkin_package()

include_directories(
  ${Boost_INCLUDE_DIRS}
  ${catkin_INCLUDE_DIRS}
)


install(DIRECTORY launch/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
    PATTERN ".svn" EXCLUDE)

add_executable(base_link_flattener
  src/base_link_costmap_projector.cpp
)

add_executable(point_cloud_filter
  src/pc_filter.cpp
)

target_link_libraries(base_link_flattener
  ${catkin_LIBRARIES}
)

target_link_libraries(point_cloud_filter
  ${catkin_LIBRARIES}
)

install(TARGETS
  base_link_flattener
  point_cloud_filter
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
# catkin_install_python(PROGRAMS 
#     scripts/serial_bridge
#     scripts/leo_system
#     DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
