add_executable(main main.cpp)
target_link_libraries(main CONAN_PKG::nlohmann_json)
