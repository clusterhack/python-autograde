# (c) 2022- Spiros Papadimitriou <spapadim@gmail.com>
#
# This file is released under the MIT License:
#    https://opensource.org/licenses/MIT
# This software is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.

# Dockerfile reconstructed from docker build output on GradeScope web UI,
#   as Dockerhub links to non-existent (404) github repo.

FROM gradescope/auto-builds:latest

RUN apt-get update && \
    apt-get install -y curl unzip dos2unix && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /autograder/source

ARG AUTOGRADER_ZIP=autograder.zip
ADD ${AUTOGRADER_ZIP} /tmp/autograder.zip

RUN unzip -n -d /autograder/source /tmp/autograder.zip

RUN cp /autograder/source/run_autograder /autograder/run_autograder

RUN dos2unix /autograder/run_autograder /autograder/source/setup.sh

RUN chmod +x /autograder/run_autograder

RUN apt-get update && \
    bash /autograder/source/setup.sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
