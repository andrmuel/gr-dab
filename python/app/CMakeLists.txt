
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
  endif()

add_custom_command(OUTPUT adjustment_gui.py COMMAND mkdir -p ${CMAKE_BINARY_DIR}/python/app
                                            COMMAND cp -r ${CMAKE_SOURCE_DIR}/python/app/*.py ${CMAKE_BINARY_DIR}/python/app/
                                            COMMAND bash -c "PYTHONPATH=${CMAKE_BINARY_DIR}/python/app GRC_BLOCKS_PATH=${CMAKE_SOURCE_DIR}/grc/ grcc ${CMAKE_SOURCE_DIR}/python/app/adjustment_gui.grc -o ${CMAKE_BINARY_DIR}/python/app/"
                                            COMMAND cp ${CMAKE_BINARY_DIR}/python/app/top_block.py ${CMAKE_BINARY_DIR}/python/app/adjustment_gui.py)
add_custom_target(run ALL DEPENDS ${CMAKE_BINARY_DIR}/python/app/adjustment_gui.py)

GR_PYTHON_INSTALL(
    FILES
    get_channels.py
    receive_dabplus.py
    config.py
    adjust_gui_helpers.py
    channel_mapping.py
    curses_app.py
    ${CMAKE_BINARY_DIR}/python/app/adjustment_gui.py
    __init__.py DESTINATION ${GR_PYTHON_DIR}/gnuradio/dab/app
)
