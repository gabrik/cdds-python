cmake_minimum_required(VERSION 3.7)
project(dds-python)

find_package(CycloneDDS)

#idlc_generate(ddsbit bit.idl)
SET(outsources)

SET(outsources bit)

list(INSERT CMAKE_MODULE_PATH 0 ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
message(" CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}")
include(idlc_generate_macro)

# find_program(idcl_generate dds_idlc /home/firas/cyclone/cyclonedds/bld/src/idlc)
# 
# if(NOT idcl_generate)
#   message(FATAL_ERROR "Failed to find idlc code generator ")
# else()
#     message("Find idlc  code generator")
# endif()

# message (${idcl_generate})
message (" outsources = ${outsources}")

message ("${idcl_generate} -d ${CMAKE_CURRENT_SOURCE_DIR}/ ${CMAKE_CURRENT_SOURCE_DIR}/${outsources}.idl")
	

# ADD_CUSTOM_COMMAND (
# OUTPUT ${outsource}.c ${outsources}.h 
# COMMAND ${idcl_generate} ARGS -d ${CMAKE_CURRENT_SOURCE_DIR} -verbose ${CMAKE_CURRENT_BINARY_DIR}/bit.idl
# COMMENT "Generating files in  ${CMAKE_CURRENT_SOURCE_DIR}  "
# )
idlc_generate_func(${CMAKE_CURRENT_SOURCE_DIR}/bit.idl)

add_library(ddstubs SHARED ${CMAKE_CURRENT_SOURCE_DIR}/dds_stubs.c)
add_library(ddsbit SHARED ${CMAKE_CURRENT_SOURCE_DIR}/bit.c ${CMAKE_CURRENT_SOURCE_DIR}/bit.h )

target_link_libraries(ddstubs ddsbit CycloneDDS::ddsc)
