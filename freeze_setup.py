# Copyright (C) 2019  DESY, Manuela Kuhn, Notkestr. 85, D-22607 Hamburg
#
# This software is free: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Manuela Kuhn <manuela.kuhn@desy.de>
#
"""
This module freezes the hidra tools to be able to run in on systems without
installing the dependencies.
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from cx_Freeze import setup, Executable


setup(name='HiDRA-tools',
      version='0.0.0',
      description='',
      executables=[Executable("get_events.py")])
