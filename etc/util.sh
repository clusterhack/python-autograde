# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

# Common utility function definitions

msg() {
  echo "$@" 1>&2
}

die() {
  msg "$@"
  exit 1
}

############################################################################

save_env() {
  # Add or replace variable definition in a simple envfile (aka dotfile)
  local VARNAME=$1
  local VALUE=$2
  local ENVFILE=${3:-env.sh}

  # TODO
}

############################################################################

install_python_apt() {
  # Install Python 3 from Ubuntu repos
  apt-get install -y python3 python3-pip python3-dev
  # python-is-python3 not available on bionic

  # Save Python executable path in envfile
  echo "export PYTHON=/usr/bin/python3" >"${AUTOGRADER_ROOT:-/autograder/source}/etc/env.sh"
  source "${AUTOGRADER_ROOT:-/autograder/source}/etc/env.sh"
}

pyenv_init() {
  # Initialize pyenv (this is also installed in .bashrc by pyenv auto-installer)
  if [[ -z "$PYENV_ROOT" ]]; then
    if [[ ! -d "$HOME/.pyenv" ]]; then
      msg "WARN: pyenv installation not found during attempt to activate!"
      return 1
    fi
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
  fi
  eval "$(pyenv init -)"  # XXX Check if virtualenv-init alone is sufficient (should be?)
  eval "$(pyenv virtualenv-init -)"
}

install_python_pyenv() {
  # Install pyenv and python 3 

  # Python build deps, per https://github.com/pyenv/pyenv/wiki#suggested-build-environment
  apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev

  # Use pyenv auto-installer
  curl https://pyenv.run | bash
  # We can't exec $SHELL (per installer instructions), but this should work instead
  pyenv_init

  # Install python via pyenv and make it the default
  pyenv install 3.9.7  # Same as Miniconda, as of 02/22/2022
  pyenv global 3.9.7

  # While at it, upgrade pip and install some packages that might come in handy
  pip install --upgrade pip

  # Save Python executable path in envfile
  echo "export PYTHON=${HOME}/.pyenv/shims/python" >"${AUTOGRADER_ROOT:-/autograder/source}/etc/env.sh"
  source "${AUTOGRADER_ROOT:-/autograder/source}/etc/env.sh"
}

############################################################################
