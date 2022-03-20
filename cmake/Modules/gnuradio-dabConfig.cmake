find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_DAB gnuradio-dab)

FIND_PATH(
    GR_DAB_INCLUDE_DIRS
    NAMES dab/api.h
    HINTS $ENV{DAB_DIR}/include
        ${PC_DAB_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_DAB_LIBRARIES
    NAMES gnuradio-dab
    HINTS $ENV{DAB_DIR}/lib
        ${PC_DAB_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-dabTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_DAB DEFAULT_MSG GR_DAB_LIBRARIES GR_DAB_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_DAB_LIBRARIES GR_DAB_INCLUDE_DIRS)
