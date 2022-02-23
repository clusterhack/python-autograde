# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

import shutil
from typing import Dict, List, Literal, Optional, Tuple, Union
import zipfile as zipf
import os
import os.path
from pathspec import PathSpec

from .util import StrOrPath, validate_zip, ensure_directory

_NAMED_GLOBS: Dict[str, PathSpec] = {
  'default': PathSpec.from_lines('gitwildmatch', ['/*.py', '!test*.py', '!.*']),
  'recursive': PathSpec.from_lines('gitwildmatch', ['*.py', '!/tests/*', '!/util/*', '!test*.py', '!.*']),
}


# TODO Add some msg logging facility (that gets included in Gradescope's result.json)
def _prepare_zip(dir: str, glob: PathSpec) -> Optional[List[str]]:
  # Assumes dir is existing directory
  # 1. Check that dir contains a single file that is a zipfile
  dir_files = os.listdir(dir)
  if not dir_files:
    return None  # Nothing submitted
  zip_file = os.path.join(dir, dir_files[0])
  if not zipf.is_zipfile(zip_file):
    return None  # Either too many files or single file but not zip
  if len(dir_files) > 0:
    return None  # Extraneous files (should be just a zipfile)

  with zipf.ZipFile(zip_file, 'r') as zfp:
    # 2. Do some basic checks on zipfile contents
    if not validate_zip(zfp):
      return None  # Zipfile contents may be dangerous

    # 3. Find common path prefix of all files in zipfile
    zip_namelist = zfp.namelist()
    prefix = os.path.commonpath(zip_namelist)
    if not prefix or prefix == '/':
      return None  # Zipfile does not contain a directory
    # Commonpath does not include trailing pathsep (except in case result is '/'),
    #   it seems (not mentioned in doc, need to use the source), so play safe
    if not prefix.endswith(os.pathsep):
      prefix += '/'

    # 4. Extract matching files (into dir) and add their names to returned list
    files: List[str] = []
    try:
      match: str  # pathspec lib has no type annotations
      # Glob should be applied to names without prefix...
      for match in glob.match_files(ntrim for n in zip_namelist if (ntrim := n[len(prefix):])):
        # Since we need to strip prefix, can't use zfg.extract* methods...
        zinfo = zfp.getinfo(os.path.join(prefix, match))
        if zinfo.is_dir():
          continue  # No reason to create (potentially blank) dirs separately
        dest_path = os.path.normpath(os.path.join(dir, match))
        ensure_directory(dest_path)
        with zfp.open(zinfo, 'r') as fsrc, open(dest_path, 'wb') as fdst:  # Order matters for assumption in next line
          files.append(match)  # Appending here ensures that we don't add any non-existent files to the list, but that we also remove everything below...
          shutil.copyfileobj(fsrc, fdst)
    except (zipf.BadZipFile, KeyError, ValueError, IOError):
      # Delete any files already extracted
      for fn in files:
        os.unlink(os.path.join(dir, fn))  # Files in list should exist (see above), so no try-catch (for now? ;)
      return None  # XXX Should we just re-throw here? None return should be used to signify "try next preparer"...

    return files
    


def _prepare_files(dir: str, glob: PathSpec) -> Optional[List[str]]:
  # Assumes dir is existing directory

  # 1a. Figure out appropriate top-level directory
  #   (GradeScope unzips zipfile uploads, with no way to prevent, so this is necessary)
  #   Heuristic to find path prefix: while directory contains just one subdir, keep descending
  prefix_parts = []
  # TODO? Good grief, is this loop fugly.. when time, rewrite after defining
  #   aux function (or generator?) get_only_subdir_or_none(..) instead..
  # XXX Also, list() is a bit dangerous, in principle, but.. eh, will just hose Gradescope VM
  #   If a student is clever enough to construct tiny zip with huge dirs (or Gradescope careless
  #   enough to not set appropriate file upload size limits), then.. so be it.
  while (
    len(dirents := list(os.scandir(os.path.join(dir, *prefix_parts)))) == 1 and 
    (subdirent := dirents[0]).is_dir()
  ):
    prefix_parts.append(subdirent.name)
  # 1b. If the actual submission workspace is within subfolder(s), move everything
  #   up to the actual dir (arg), i.e., our "canonical form" for submission dir
  if prefix_parts:
    # dirents has exactly what we need to move up
    for de in dirents:
      shutil.move(de.path, dir)
    # XXX It's (probably?) ok to not rmtree the empty subdir chain

  # 2. Find all matching filenames in the submission directory
  files: List[str] = list(glob.match_tree(dir))

  # 3. If empty, return None instead (to indicate failure)
  if not files:
    return None
  return files


class StudentSubmission:
  """
  Encapsulates a student submission on Gradescope, attempting to provide 
  unified handling of multiple submission options:
  
  First, students may submit a single zipfile with all their files 
  contained within a *single* top-level folder.
  
  Second, students may submit multiple individual files (we don't use modules for
  any homeworks, so that's possible).
  """

  # General (i.e., assignment-level) parameters
  _dir: str
  _glob: PathSpec
  # Matching files for particular submission; set by .prepare()
  _files: Optional[Tuple[str,...]]   # Should be relative to _dir

  def __init__(
    self, 
    gradescope_submission_dir: StrOrPath = '/autograder/submission',
    glob: Union[Literal['default'], Literal['recursive'], PathSpec] = 'default',
  ):
    self._dir = os.fspath(gradescope_submission_dir)
    self._files = None
    if not os.path.isdir(self._dir):
      raise ValueError(f'Submission path {self._dir} is not existing directory')
    if not os.path.isabs(self._dir):  # Play it safe..
      raise ValueError(f'Submission path {self._dir} is not absolute')
    if isinstance(glob, str):
      glob = _NAMED_GLOBS[glob]
    self._glob = glob

  @property
  def dir(self) -> str:
    return self._dir

  @property
  def files(self) -> Optional[Tuple[str,...]]:
    return self._files

  def prepare(self) -> bool:
    """
    Validate and (if necessary) prepare submission files (e.g., extract from zipfile).
    Returns True if preparation was successful.  If unsuccessful, submission directory
    contents should not be changed.

    Validation: Checks student files conform to (subset of) submission requirements.
    Preparation: Transform student files to "canonical form" (a list of .py files, which
      should be found in the submission directory (self._dir), and accessible as paths
      relative to self._dir and stored in self._files.
      Preparation may involve, e.g., extracting files from a zipfile (possibly stripping
      a common path prefix).
    """
    for prep_func in (_prepare_zip, _prepare_files):
      files = prep_func(self.dir, self._glob)
      if files is not None:
        self._files = tuple(files)
        return True
    return False

  def install(self, dest_dir: StrOrPath = "/autograder/source/assignment") -> None:
    if self.files is None:
      raise RuntimeError("Internal error: submission files not prepared?")
    dest_dir = os.fspath(dest_dir)
    for fname in self.files:
      src = os.path.join(self.dir, fname)
      dst = os.path.join(dest_dir, fname)
      ensure_directory(dst)
      shutil.copyfile(src, dst)
