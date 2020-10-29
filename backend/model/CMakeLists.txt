cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(loss)

list(APPEND CMAKE_PREFIX_PATH "$HOME/libtorch")
find_package(Torch REQUIRED)

add_executable(loss loss.cpp)
target_link_libraries(loss "${TORCH_LIBRARIES}")
set_property(TARGET loss PROPERTY CXX_STANDARD 14)