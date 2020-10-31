cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(loss)

list(APPEND CMAKE_PREFIX_PATH "/home/daksh/libtorch")
find_package(Torch REQUIRED)

add_executable(${EXECUTABLE_NAME})
target_sources(${EXECUTABLE_NAME} PRIVATE src/main.cpp
                                          src/loss.cpp
                                          src/resnet.cpp
                                          include/resnet.h
                                          include/loss.h
)


target_include_directories(${EXECUTABLE_NAME} PRIVATE include)

target_link_libraries(loss "${TORCH_LIBRARIES}")
set_property(TARGET loss PROPERTY CXX_STANDARD 14)