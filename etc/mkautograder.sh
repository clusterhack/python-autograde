#! /bin/bash

# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

TARGET=$(realpath -m "${1:-../autograder.zip}")  # since we cd next...

# Set cwd to project root ( == script's parent directory)
cd "$( dirname "${BASH_SOURCE[0]}" )"/.. 

. etc/util.sh
. etc/env.sh

msg "INFO: Cwd set to $(pwd)"
msg "INFO: Target zipfile is ${TARGET}"

if [[ -f "${TARGET}" ]]; then
  msg "WARN: Previous zipfile exists; deleting"
  rm "${TARGET}"
fi

zip -9r "${TARGET}" . \
  -x'etc/*.ctx/*' -x'attic/*' -x'assignment/*' \
  -x'.vscode/*' -x'.git/*'
