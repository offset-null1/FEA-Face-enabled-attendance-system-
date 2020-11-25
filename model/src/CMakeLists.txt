if(NOT TARGET model)
    add_library(LibModel SHARED 
    ${CMAKE_SOURCE_DIR}/src/load.cpp  
    ${CMAKE_SOURCE_DIR}/src/metric.cpp 
    ${CMAKE_SOURCE_DIR}/src/train.cpp)
endif()
target_include_directories(LibModel PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../include)

target_link_libraries(LibModel "${TORCH_LIBRARIES}")
target_link_libraries(LibModel ${OpenCV_LIBS})
target_link_libraries(LibModel -lstdc++fs)
