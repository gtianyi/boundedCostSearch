add_executable(bcs main.cpp)
target_link_libraries(bcs CONAN_PKG::nlohmann_json CONAN_PKG::cxxopts)
