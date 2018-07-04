gr-dab
======

```
 gr-dab - GNU Radio Digital Audio Broadcasting module
 Copyright (C) Andreas Müller, 2011, Moritz Luca Schmid, 2017

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
```


This directory (and the resulting tarball) contains a build tree for
gr-dab.

gr-dab contains everything needed to get audio from DAB and DAB+

Much of the code was developed as part of "Google Summer of Code 2017" by
Moritz Luca Schmid. (the completion of audio reception of DAB and DAB+)

This package requires that gnuradio-core is already installed.  It
also depends on some GNU Radio prerequisites, such as Boost and
cppunit. Additionally it depends on the FAAD2 library. (ubuntu: sudo apt-get
install libfaad-dev, fedora: sudo dnf install faad2-devel)

To build the examples from the tarball run these commands:

```
  $ mkdir build
  $ cd build
  $ cmake ../
  $ make
  $ sudo make install
  $ sudo ldconfig
```

Additional notes
----------------

To build gr-dab, please take into account:

* gr-dab does not work with GNU Radio 3.3; I usually work with the master
  branch from the GNU Radio git repository

* for the simulations in python/channel_tests/, you need the following
  additional dependencies:
   * the patches in the patches directory (except for the patches in
     'applied_in_trunk') must be applied to the GNU Radio trunk
   * Scipy (available from http://scipy.sourceforge.net)
   * Matplotlib (available from http://matplotlib.sourceforge.net)
