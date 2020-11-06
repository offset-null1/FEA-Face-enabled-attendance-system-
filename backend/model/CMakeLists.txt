cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(model)

find_package(Torch REQUIRED)

include_directories(include)

file(GLOB SOURCES "src/*.cpp")
add_executable(model ${SOURCES})

add_executable(model main.cpp)

target_link_libraries(model "${TORCH_LIBRARIES}")

set_property(TARGET model PROPERTY CXX_STANDARD 14)
