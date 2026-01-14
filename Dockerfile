FROM ubuntu:22.04
LABEL maintainer="Neal Magee <nem2p@virginia.edu>"

ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=myuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG GROUPNAME=mygroup
ENV TZ=America/New_York

RUN groupadd --gid $USER_GID $GROUPNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
# Ensure the user is in the docker group for DinD (group will be created by docker-in-docker feature)
RUN groupadd -f docker && usermod -aG docker $USERNAME

RUN apt-get install -y software-properties-common curl
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip nano \
  git net-tools jq zip unzip dnsutils httpie tzdata wget htop \
  iputils-ping redis-server apt-transport-https pkg-config \
  ca-certificates gnupg gcc python3-setuptools libffi-dev \
  mongodb-org libmysqlclient-dev groff \
  && apt-get clean autoclean && apt-get autoremove --yes \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Install man-db and documentation packages
# Note: unminimize can be problematic in non-interactive builds, so we install man pages directly
RUN apt-get update && apt-get install -y --no-install-recommends \
    man-db manpages manpages-dev manpages-posix manpages-posix-dev \
    && apt-get clean

# Create python symlink (Ubuntu 22.04 comes with Python 3.10)
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Cleanup apt lists (redundant but harmless - already cleaned in previous step)
RUN rm -rf /var/lib/apt/lists/*
RUN mkdir "/home/host"

WORKDIR /root
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt
