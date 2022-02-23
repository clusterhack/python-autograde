# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

import os
import sys
import unittest

from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

from .util import StrOrPath


def run_tests(
  assignment_dir: StrOrPath = '/autograder/source/assignment', 
  results_file: StrOrPath = '/autograder/results/results.json'
) -> None:
  assignment_dir = os.fspath(assignment_dir)

  if not os.path.isdir(assignment_dir):
    raise ValueError(f'Assignment root f{assignment_dir} is not an existing directory')
  if not os.path.isabs(assignment_dir):  # Play it safe..
    raise ValueError(f'Assignment root path f{assignment_dir} is not absolute')
  
  # For backwards compatibility with pre-GradeScope setup...
  # TODO XXX We should handle this a bit better/safer (multiprocessing perhaps, or just fork)
  if assignment_dir not in sys.path:
    sys.path.append(assignment_dir)
  os.chdir(assignment_dir)  # Possibly don't need to chdir? Can't hurt..

  # Run unit tests
  suite = unittest.defaultTestLoader.discover('.', pattern='test_*.py')
  with open(results_file, 'w') as fp:
    JSONTestRunner(visibility='visible', stream=fp).run(suite)
