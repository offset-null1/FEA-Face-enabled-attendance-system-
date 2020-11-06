cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(model)

find_package(Torch REQUIRED)

include_directories(include)
<<<<<<< HEAD
file(GLOB SOURCES "src/*.cpp")
add_executable(model ${SOURCES})
=======
>>>>>>> de3a5ae... model+cmake

add_executable(model main.cpp)

<<<<<<< HEAD

target_link_libraries(model "${TORCH_LIBRARIES}")
=======
target_link_libraries(model "${TORCH_LIBRARIES}")

>>>>>>> de3a5ae... model+cmake
set_property(TARGET model PROPERTY CXX_STANDARD 14)