cmake_minimum_required(VERSION 3.12)
project(test_package LANGUAGES CXX)

find_package(kdl_parser CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE kdl_parser::kdl_parser)
