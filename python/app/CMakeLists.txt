
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
  endif()


GR_PYTHON_INSTALL(
    FILES
    get_channels.py
    receive_dabplus.py
    config.py
    tune_gain_and_ppm.py
    __init__.py DESTINATION ${GR_PYTHON_DIR}/grdab/app
)
