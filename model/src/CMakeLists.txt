find_package(OpenCV 4.1.0 REQUIRED)
# find_package(HDF5)
set (LIB_TYPE STATIC) # or SHARED
string(TOLOWER ${LIB_TYPE} SEARCH_TYPE)
FIND_PACKAGE(HDF5 COMPONENTS C HL NO_MODULE REQUIRED shared)

find_package (HDF5 NAMES hdf5 COMPONENTS C ${SEARCH_TYPE})
# find_package (HDF5) # Find non-cmake built HDF5
INCLUDE_DIRECTORIES (${HDF5_INCLUDE_DIR})
set (LINK_LIBS ${LINK_LIBS} ${HDF5_C_${LIB_TYPE}_LIBRARY})

add_compile_definitions(${HDF5_CXX_DEFINITIONS})

if(NOT TARGET model)
    add_library(LibModel STATIC
    ${CMAKE_SOURCE_DIR}/src/load.cpp  
    ${CMAKE_SOURCE_DIR}/src/metric.cpp 
    ${CMAKE_SOURCE_DIR}/src/train.cpp)
endif()

include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(HDF5_CXX_INCLUDE_DIRS)
include_directories(HDF5_INCLUDE_DIRS)
target_include_directories(LibModel PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../include)

target_link_libraries(LibModel "${TORCH_LIBRARIES}")
target_link_libraries(LibModel ${OpenCV_LIBS})
target_link_libraries(LibModel ${HDF5_LIBRARIES})
target_link_libraries(LibModel ${HDF5_HL_LIBRARIES})
target_link_libraries(LibModel ${HDF5_CXX_LIBRARIES})
target_link_libraries(LibModel -lstdc++fs)

# target_link_libraries(LibModel "/usr/share/doc/libhdf5-dev")
# target_link_libraries(LibModel -lhdf5_cpp)
# target_link_libraries(LibModel -lhdf5_hl)
enable_testing ()
include (CTest)