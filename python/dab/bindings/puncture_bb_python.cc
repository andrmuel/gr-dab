/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(puncture_bb.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(38cb4879664fed8ee508a0a503cf74eb)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <dab/puncture_bb.h>
// pydoc.h is automatically generated in the build directory
#include <puncture_bb_pydoc.h>

void bind_puncture_bb(py::module& m)
{

    using puncture_bb    = ::gr::dab::puncture_bb;


    py::class_<puncture_bb, gr::block, gr::basic_block,
        std::shared_ptr<puncture_bb>>(m, "puncture_bb", D(puncture_bb))

        .def(py::init(&puncture_bb::make),
           py::arg("puncturing_vector"),
           D(puncture_bb,make)
        )
        



        ;




}








