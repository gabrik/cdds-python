#
# Copyright(c) 2006 to 2018 ADLINK Technology Limited and others
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v. 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0, or the Eclipse Distribution License
# v. 1.0 which is available at
# http://www.eclipse.org/org/documents/edl-v10.php.
#
# SPDX-License-Identifier: EPL-2.0 OR BSD-3-Clause
#



#set(IDLC_DIR "${CMAKE_CURRENT_BINARY_DIR}" CACHE STRING "")
#set(IDLC "dds_idlc${EXTENSION}" CACHE STRING "")
#mark_as_advanced(IDLC_DIR IDLC)

#set(IDLC_SCRIPT_IN "${CMAKE_CURRENT_LIST_DIR}/dds_idlc${EXTENSION}.in")

#configure_file(
#    "${IDLC_SCRIPT_IN}" "${IDLC}"
#    @ONLY
#    NEWLINE_STYLE ${LINE_ENDINGS})
#
#if(NOT ("${CMAKE_SYSTEM_NAME}" STREQUAL "Windows"))
#    execute_process(COMMAND chmod +x "${IDLC_DIR}/${IDLC}")
#endif()

#add_custom_target(idlc ALL DEPENDS "${IDLC_JAR}")

MACRO (idlc_generate_func idl_file)
  message("idl_file: ${idl_file} ")
  
  if(idl_file STREQUAL "")
    message(FATAL_ERROR "idlc_generate called without any idl files")
  endif()

  if (NOT IDLC_ARGS)
     set(IDLC_ARGS)
  endif()

  set(_dir "${CMAKE_CURRENT_BINARY_DIR}")
  set(_sources)
  set(_headers)
  
  find_program(idcl_generate_full_path 
  				dds_idlc 
  				PATHS /home/firas/cyclone/cyclonedds/bld/src/idlc)

   	if( idcl_generate_full_path STREQUAL "")
		message(FATAL_ERROR "Failed to find idlc code generator ")
	else()
		message("${idcl_generate_full_path}: Found idlc  code generator")
	endif()
  
  foreach(FIL ${idl_file})
  	message("file to parse ${FIL} ")
    get_filename_component(ABS_FIL ${FIL} ABSOLUTE)
    get_filename_component(FIL_WE ${FIL} NAME_WE)

    set(_source "${CMAKE_CURRENT_SOURCE_DIR}/${FIL_WE}.c")
    set(_header "${CMAKE_CURRENT_SOURCE_DIR}/${FIL_WE}.h")
    
    list(APPEND _sources "${_source}")
    list(APPEND _headers "${_header}")

    add_custom_command(
      OUTPUT   "${_source}" "${_header}"
      COMMAND  "${idcl_generate_full_path}"
      ARGS     -d ${CMAKE_CURRENT_SOURCE_DIR} ${ABS_FIL}
      COMMENT  "Running idlc on ${FIL}"
      VERBATIM)
  endforeach()
  
  message("sources ${_sources}" )
  message("headers ${_headers}" )
  
  set_source_files_properties(${_sources} ${_headers} PROPERTIES GENERATED TRUE)
  
endmacro()

