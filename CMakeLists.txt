cmake_minimum_required(VERSION 3.14)

project(BoundedCostSearch LANGUAGES C CXX)

# Project wide C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(DCMAKE_BUILD_TYPE Debug)

option(BUILD_TESTS "Build Tests" ON)

message(STATUS "Build type: " ${CMAKE_BUILD_TYPE})

enable_testing()

# Declare a convenience function to create tests
#include(add_test_executable)

# Dynamic libraries preferred by default
option(BUILD_SHARED_LIBS "Build shared libraries" ON)

# Put all binaries and libraries in the same place
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Convenience default settings for install destinations. Use it to
# install targets to the right place. For instance:
#
#    add_library(mylib)
#    install(TARGETS mylib ${DEFAULT_DESTINATIONS})
#
# It will purposely not install static libraries, since they are
# not needed once the project has been deployed.
# cmake-format: off
set(DEFAULT_DESTINATIONS
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib EXCLUDE_FROM_ALL
    OBJECTS DESTINATION lib EXCLUDE_FROM_ALL)

add_compile_options(
    -Wall -Wextra           # Typical baseline
    -Wpedantic              # Non-standard C++ is used

    -Wshadow                # Variable declaration shadows one from a parent scope
    -Wnon-virtual-dtor      # Class with virtual functions has a non-virtual destructor
    -Wold-style-cast        # C-style casts
    -Wcast-align            # Potential errors dereferencing pointers
    -Woverloaded-virtual    # Overload (not override) a virtual function
    -Wconversion            # Type conversions that may lose data
    -Wsign-conversion       # Sign conversions
    -Wdouble-promotion      # float is implicit promoted to double
    -Wformat=2              # Security issues around functions that format output (like printf)
    )
# cmake-format: on

#This allows colored output and error highlighting
#when building from command - line, for both
if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    add_compile_options(-fdiagnostics-color=always)
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    add_compile_options(-fcolor-diagnostics)
endif()

# Treat warnings as errors unless in DEVELOPMENT_MODE
option(ENABLE_WERROR "Warnings treated as errors" ON)
if(ENABLE_WERROR)
    add_compile_options(-Werror)
endif()

option(ENABLE_DOXYGEN "Use Doxygen to generate documentation by providing 'make doc'." OFF)
if(ENABLE_DOXYGEN)
    include(doxygen)
    enable_doxygen()
endif()

add_subdirectory(src)
