cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(model)

list(APPEND CMAKE_PREFIX_PATH "/home/daksh/libtorch")
find_package(Torch REQUIRED)

include_directories(include)
file(GLOB SOURCES "src/*.cpp")
add_executable(model ${SOURCES})



target_link_libraries(model "${TORCH_LIBRARIES}")
set_property(TARGET model PROPERTY CXX_STANDARD 14)