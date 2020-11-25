cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(model)

find_package(Torch REQUIRED)
find_package(OpenCV 4.1.0 REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

if (NOT TARGET model)
    add_subdirectory("${CMAKE_SOURCE_DIR}/src")
    list(APPEND EXTRA_LIBS LibModel)
    list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/include")
endif()

link_directories(${MyProject_SOURCE_DIR}/src)

add_executable(${PROJECT_NAME} main.cpp)


target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} "${TORCH_LIBRARIES}")
target_link_libraries(${PROJECT_NAME} ${EXTRA_LIBS})

target_include_directories(${PROJECT_NAME} PUBLIC ${EXTRA_INCLUDES})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})

set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 17)

