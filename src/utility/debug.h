#ifdef DEBUG
#define DEBUG_MSG(str)                                                         \
    do {                                                                       \
        std::cerr << str << std::endl;                                         \
    } while (false)
#else
#define DEBUG_MSG(str)                                                         \
    do {                                                                       \
    } while (false)
#endif
