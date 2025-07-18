cmake_minimum_required(VERSION 3.7.2)

project(kdl_parser)

set(CMAKE_CXX_STANDARD 17)

find_package(catkin QUIET COMPONENTS rosconsole cmake_modules)
if(catkin_FOUND)

  find_package(urdfdom REQUIRED)
  include_directories(${urdfdom_INCLUDE_DIRS})

  find_package(orocos_kdl REQUIRED)
  find_package(TinyXML REQUIRED)
  find_package(TinyXML2 REQUIRED)

  # check for rosconsole We check additionally for catkin to distinguish between
  # an "official" ROS distribution and the one provided in the distribution's
  # repository.
  find_package(rosconsole QUIET)

  if(rosconsole_FOUND)
    add_definitions(-DHAS_ROS)
  endif()

  find_package(urdf QUIET)
  if(urdf_FOUND)
    add_definitions(-DHAS_URDF)
    include_directories(${urdf_INCLUDE_DIRS})
  endif()

  include_directories(include ${orocos_kdl_INCLUDE_DIRS}
                      ${TinyXML_INCLUDE_DIRS} ${TinyXML2_INCLUDE_DIRS})

  link_directories(${catkin_LIBRARY_DIRS})
  include_directories(${catkin_INCLUDE_DIRS})

  catkin_package(
    LIBRARIES
    ${PROJECT_NAME}
    ${orocos_kdl_LIBRARIES}
    INCLUDE_DIRS
    include
    CATKIN_DEPENDS
    rosconsole
    urdf
    DEPENDS
    orocos_kdl
    TinyXML
    TinyXML2)

  add_library(${PROJECT_NAME} SHARED src/kdl_parser.cpp)
  target_link_libraries(${PROJECT_NAME} ${TinyXML_LIBRARIES}
                        ${TinyXML2_LIBRARIES} ${orocos_kdl_LIBRARIES})

  target_link_libraries(${PROJECT_NAME} ${urdfdom_LIBRARIES})

  target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES})

  if(urdf_FOUND)
    target_link_libraries(${PROJECT_NAME} ${urdf_LIBRARIES})
  endif()

  if(WIN32)
    target_compile_definitions(${PROJECT_NAME}
                               PRIVATE "KDL_PARSER_BUILDING_DLL")
  endif()

  add_executable(check_kdl_parser src/check_kdl_parser.cpp)
  target_link_libraries(check_kdl_parser ${PROJECT_NAME})

  if(CATKIN_ENABLE_TESTING)
    find_package(catkin REQUIRED COMPONENTS roscpp rostest)
    add_rostest_gtest(test_kdl_parser test/test_kdl_parser.launch
                      test/test_kdl_parser.cpp)
    target_link_libraries(test_kdl_parser ${PROJECT_NAME})

    add_rostest_gtest(test_inertia_rpy test/test_inertia_rpy.launch
                      test/test_inertia_rpy.cpp)
    target_link_libraries(test_inertia_rpy ${PROJECT_NAME})
  endif()

  # How does CATKIN do this?
  # rosbuild_add_rostest(${PROJECT_SOURCE_DIR}/test/test_kdl_parser.launch)

  # Install library
  install(
    TARGETS ${PROJECT_NAME}
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION})

  install(DIRECTORY include/${PROJECT_NAME}/
          DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION})
else()

  find_package(urdfdom CONFIG REQUIRED)
  find_package(orocos-kdl CONFIG REQUIRED)
  find_package(tinyxml REQUIRED CONFIG)
  find_package(tinyxml2 REQUIRED CONFIG)
  add_library(${PROJECT_NAME} src/kdl_parser.cpp)

  if(WIN32)
    set(BUILD_SHARED_LIBS ON)
    target_compile_definitions(${PROJECT_NAME} PUBLIC "KDL_PARSER_BUILDING_DLL")
  endif()

  target_include_directories(
    ${PROJECT_NAME}
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
           $<INSTALL_INTERFACE:include>)
  target_link_libraries(
    ${PROJECT_NAME} PUBLIC urdfdom::urdfdom orocos-kdl::orocos-kdl
                           tinyxml::tinyxml tinyxml2::tinyxml2)

  set(KDL_PARSER_PUBLIC_HEADERS "include/kdl_parser/kdl_parser.hpp"
                                "include/kdl_parser/visibility_control.hpp")

  set_target_properties(${PROJECT_NAME}
                        PROPERTIES PUBLIC_HEADER "${KDL_PARSER_PUBLIC_HEADERS}")
  install(TARGETS ${PROJECT_NAME}
          PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/kdl_parser)

  if(NOT BUILD_TESTING STREQUAL OFF)
    enable_testing()

    find_package(GTest REQUIRED)
    include_directories(${GTEST_INCLUDE_DIRS})
    include(GoogleTest)

    add_executable(test_kdl_parser test/test_kdl_parser.launch
                                   test/test_kdl_parser.cpp)
    target_compile_definitions(
      test_kdl_parser
      PRIVATE ROBOT_URDF="${CMAKE_CURRENT_SOURCE_DIR}/test/test_robot.urdf")
    target_link_libraries(test_kdl_parser ${PROJECT_NAME} GTest::gtest_main)
    gtest_add_tests(TARGET test_kdl_parser)

    add_executable(test_inertia_rpy test/test_inertia_rpy.launch
                                    test/test_inertia_rpy.cpp)
    target_compile_definitions(
      test_inertia_rpy
      PRIVATE
        RPY_URDF1="${CMAKE_CURRENT_SOURCE_DIR}/test/testInertiaRPYmodel1.urdf"
        RPY_URDF2="${CMAKE_CURRENT_SOURCE_DIR}/test/testInertiaRPYmodel2.urdf")
    target_link_libraries(test_inertia_rpy ${PROJECT_NAME} GTest::gtest_main)
    gtest_add_tests(TARGET test_inertia_rpy)
  endif()

endif()
