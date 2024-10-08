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
/* BINDTOOL_HEADER_FILE(modulo_ff.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(233a147da6ff5a1ae995046e32f48c6b)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <dab/modulo_ff.h>
// pydoc.h is automatically generated in the build directory
#include <modulo_ff_pydoc.h>

void bind_modulo_ff(py::module& m)
{

    using modulo_ff    = ::gr::dab::modulo_ff;


    py::class_<modulo_ff, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<modulo_ff>>(m, "modulo_ff", D(modulo_ff))

        .def(py::init(&modulo_ff::make),
           py::arg("div"),
           D(modulo_ff,make)
        )
        



        ;




}








