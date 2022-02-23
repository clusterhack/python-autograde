# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

from typing import List, Union
import os
import os.path
from zipfile import ZipFile, ZipInfo

StrOrPath = Union[str, os.PathLike]


def ensure_directory(path: StrOrPath):
  """Ensure parent directory of given pathname exists"""
  parent_path = os.path.dirname(path)
  if parent_path and not os.path.exists(parent_path):
    os.makedirs(parent_path)

def validate_zip_member(member: ZipInfo) -> bool:
  """
  Perform basic security checks on a zipfile member, similar to 
  those in ZipFile._extract_member (in fact, most of this function
  is copied from there).
  """
  # Try to make os.path functions work with member name
  arcname = member.filename.replace('/', os.path.sep)
  if os.path.altsep:
    arcname = arcname.replace(os.path.altsep, os.path.sep)
  # Reject if there is a drive letter
  if os.path.splitdrive(arcname)[0]:
    return False
  # Reject if there are any invalid path components
  if any(part in ('', os.path.curdir, os.path.pardir) for part in arcname.split(os.path.sep)):
    return False
  return True
  

def validate_zip(zipfile_or_members: Union[ZipFile, List[ZipInfo]]) -> bool:
  """
  Utility function to validate every member of a zipfile, using
  validate_zip_member.
  """
  if isinstance(zipfile_or_members, ZipFile):
    members = zipfile_or_members.infolist()
  else:
    members = zipfile_or_members
  for m in members:
    if not validate_zip_member(m):
      return False
  return True
