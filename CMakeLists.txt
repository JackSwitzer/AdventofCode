cmake_minimum_required(VERSION 3.29)
project(AdventOfCode C)

set(CMAKE_CXX_STANDARD 14)

add_executable(day5 Days/5.c)

# Copy data file to build directory
configure_file(${CMAKE_SOURCE_DIR}/Data/5.txt ${CMAKE_BINARY_DIR}/Data/5.txt COPYONLY)
