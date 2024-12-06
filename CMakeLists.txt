cmake_minimum_required(VERSION 3.10)
project(AdventOfCode LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(AdventOfCode Days/6.cpp)

# Copy data file to build directory
configure_file(${CMAKE_SOURCE_DIR}/Data/5.txt ${CMAKE_BINARY_DIR}/Data/5.txt COPYONLY)
