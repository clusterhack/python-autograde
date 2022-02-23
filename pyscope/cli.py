# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

import click
import json

from .submission import StudentSubmission
from .testrunner import run_tests

# TODO Should add proper config support (dataclass-based, probably)...

@click.group()
def main():
  pass

@main.command()
def setup():
  sub = StudentSubmission()
  click.echo("Preparing student submission files...")
  if not sub.prepare():
    # TODO Re-do this properly (and extend it), once we get rid of gradescope-utils
    #   This bit is done in a hurry, to show *something* to student
    #   We should also adding info messages upon success (saying, e.g., what files we found)
    #     but gradescope-utils doesn't really allow this (since result output facilities are 
    #     'bolted onto' test runs -- there is a JSON post-processing hook on runner, but
    #      we can only use that *after* the test runner completes a run, without barfing...)
    with open('/autograder/results/results.json', 'w') as fp:
      result = {
        "score": 0.0,
        "output":
          "Malformed submission; giving up!\n"
          "You should either upload a zipfile of the workspace *folder*, "
          "or individual .py files.",
      }
      json.dump(result, fp, indent=2)
    raise click.FileError("Malformed submission")
  click.echo("Installing student submission files...")
  sub.install()

@main.command()
def unittest():
  click.echo("Running unit tests...")
  run_tests()


if __name__ == '__main__':
  main()
