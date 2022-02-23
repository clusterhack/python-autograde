# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

# This file is required by gradescope, and will be copied
# to the abs path /autograder/run_autograder. It's executed
# by Gradescope's dockerfile.

# Fail with error if not running in Docker..
if ! grep -sq ':/\(docker\|lxc\)' /proc/1/cgroup; then
  echo "ERROR: Not running in a container!" 1>&2
  exit 1
fi

# set -x  # xtrace on

# All files (incl. this, i.e., setup.sh) will remain
# within abs path /autograder/source on the Docker image
export AUTOGRADER_ROOT=/autograder/source
cd ${AUTOGRADER_ROOT}
. etc/util.sh

# Choose one of the two...
msg "INFO: Installing Python; this may take a while..."
# install_python_apt  # DANGER: Gradescope still uses bionic (18.04).. !!!
install_python_pyenv
# TODO? Add miniconda option...

# Install BSD tar (easy way to strip leading path components when extracting zipfiles)
msg "INFO: Installing utilities"
apt-get install -y libarchive-tools 

# Create empty 'assignment' subdirectory, if not already there
if [[ ! -d assignment ]]; then
  if [[ -f assignment ]]; then
    die "FATAL: 'assignment' already exists, but is not a directory"
  fi
  msg "INFO: Creating empty 'assignment' directory"
  mkdir assignment
else
  msg "INFO: 'assignment' directory already exists; not touching"
fi

# For backwards compatibility with pre-Gradescope setup, we can just append a skeleton file 
#   (created with the old mkzip.sh, which zips the workspace *folder*, not it's contents)
#   into the autograder zip. If so, file should be named 'skeleton.zip'.
if [[ -f skeleton.zip ]]; then
  msg "INFO: Found skeleton zipfile, extracting into 'assignment' (stripping top-level directory)"
  bsdtar -xvf skeleton.zip --strip-components 1 --exclude '.vscode/*' --cd assignment
fi

msg "INFO: Installing Python requirements"
pip install -r requirements.txt

# TODO Remove ${HOME}/.cache/pip (just ~150KB for now, and still trialing stuff...)
