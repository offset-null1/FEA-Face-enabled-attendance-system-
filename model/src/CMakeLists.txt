find_package(OpenCV 4.1.0 REQUIRED HINTS "/usr/local/share/OpenCV")
find_package(hdf5)
# set (LIB_TYPE STATIC) # or SHARED
# string(TOLOWER ${LIB_TYPE} SEARCH_TYPE)
# FIND_PACKAGE(HDF5 COMPONENTS C HL NO_MODULE REQUIRED shared)

# find_package (HDF5 NAMES hdf5 COMPONENTS C ${SEARCH_TYPE})
# find_package (HDF5) # Find non-cmake built HDF5
# INCLUDE_DIRECTORIES (${HDF5_INCLUDE_DIR})
# set (LINK_LIBS ${LINK_LIBS} ${HDF5_C_${LIB_TYPE}_LIBRARY})

# add_compile_definitions(${HDF5_CXX_DEFINITIONS})

if(NOT TARGET model)
    add_library(LibModel STATIC
    ${CMAKE_SOURCE_DIR}/src/load.cpp  
    ${CMAKE_SOURCE_DIR}/src/metric.cpp 
    ${CMAKE_SOURCE_DIR}/src/train.cpp
    )
endif()

include_directories(${OpenCV_INCLUDE_DIRS})
message(STATUS " OPENCV INCLUDES: ${OpenCV_INCLUDE_DIRS}")

# include_directories(HDF5_CXX_INCLUDE_DIRS)
# include_directories(HDF5_INCLUDE_DIRS)

# target_link_libraries(LibModel ${HDF5_LIBRARIES})
# target_link_libraries(LibModel ${HDF5_HL_LIBRARIES})
# target_link_libraries(LibModel ${HDF5_CXX_LIBRARIES})

# target_link_libraries(LibModel "/usr/share/doc/libhdf5-dev")
# target_link_libraries(LibModel -lhdf5_cpp)
# target_link_libraries(LibModel -lhdf5_hl)
# enable_testing ()
# include (CTest)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR})

if(WIN32)
  # windows cmake internal lookups are broken for now
  # will lookup for headers and shared libs given HDF_DIR env
  find_path(HDF5_INCLUDE_DIRS hdf5.h HINTS "$ENV{HDF5_DIR}\\..\\include")
  find_library(HDF5_C_LIBRARY NAMES hdf5 HINTS "$ENV{HDF5_DIR}\\..\\lib")
  if(HDF5_INCLUDE_DIRS AND HDF5_C_LIBRARY)
    set(HDF5_FOUND "YES")
    set(HDF5_LIBRARIES ${HDF5_C_LIBRARY})
    mark_as_advanced(HDF5_LIBRARIES)
    mark_as_advanced(HDF5_C_LIBRARY)
    mark_as_advanced(HDF5_INCLUDE_DIRS)
    add_definitions(-DH5_BUILT_AS_DYNAMIC_LIB -D_HDF5USEDLL_)
  else()
     set(HDF5_FOUND "NO")
  endif()
else()
  if(NOT CMAKE_CROSSCOMPILING) # iOS build should not reuse OSX package
    find_package(HDF5)
  endif()
endif()

if(NOT HDF5_FOUND)
    ocv_module_disable(hdf) # no return
endif()

set(HAVE_HDF5 1)

# ocv_warnings_disable(CMAKE_CXX_FLAGS -Winvalid-offsetof)

set(the_description "Hierarchical Data Format I/O")
# ocv_define_module(hdf opencv_core WRAP python)
include_directories(${HDF5_INCLUDE_DIRS})

target_include_directories(LibModel PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../include)

target_link_libraries(LibModel "${TORCH_LIBRARIES}")
target_link_libraries(LibModel ${HDF5_LIBRARIES})

target_link_libraries(LibModel ${OpenCV_LIBS})
target_link_libraries(LibModel -lstdc++fs)
