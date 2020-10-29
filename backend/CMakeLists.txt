cmake_minimum_required(VERSION 3.0.0 FATAL_ERROR)
project(torchtest VERSION 0.1.0)

find_package("/home/daksh/libtorch" REQUIRED)

include(CTest)
enable_testing()

add_executable(torchtest torchtest.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)

target_link_libraries(torchtest "${TORCH_LIBRARIES}")
set_property(TARGET torchtest PROPERTY CXX_STANDARD 14)