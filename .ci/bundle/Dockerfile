FROM p4a/build-env

ENV WORKDIR /root/bundle
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR

##############################
# Download the recipe set

ARG recipe_tarball_url=https://github.com/F1uctus/p4a-recipes/tarball/c6c9906b87a8fed8f5680b1f7fdc5eec32b958ff

RUN wget $recipe_tarball_url -O p4a-recipes.tgz \
 && mkdir local_recipes \
 && tar -xz --strip-components=1 -f p4a-recipes.tgz -C local_recipes \
 && rm p4a-recipes.tgz

RUN mkdir src && > src/main.py

##############################
# Install project build dependencies

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
	libc6-dev \
	libgdbm-dev \
	libncursesw5-dev \
	lld \
	openssl \
 && apt -y autoremove \
 && apt -y clean \
 && rm -rf /var/lib/apt/lists/*

##############################
# Install essential python packages

RUN python3 -m pip install -U \
	pip setuptools wheel cython

##############################
# Build the project

VOLUME /root/.local/share
VOLUME /root/.ccache

ARG python_version="3.10.5"
ENV PROJECT_PYTHON_VERSION=$python_version

ENV PROJECT_PYTHON_REQUIREMENTS="\
hostpython3==${PROJECT_PYTHON_VERSION},\
python3==${PROJECT_PYTHON_VERSION},"

ARG requirements="spacy"
ENV PROJECT_REQUIREMENTS=$requirements

ARG arch="arm64-v8a"
ENV PROJECT_ARCH=$arch

ARG min_android_api="24"
ENV PROJECT_NDK_API=$min_android_api

ENTRYPOINT p4a apk \
	--release \
	--private $WORKDIR/src \
	--name bundle \
	--version 1.0 \
	--package org.p4a.bundle \
	--bootstrap service_only \
	--requirements "${PROJECT_PYTHON_REQUIREMENTS}${PROJECT_REQUIREMENTS}" \
	--blacklist-requirements android,sqlite3 \
	--local-recipes $WORKDIR/local_recipes \
	--arch $PROJECT_ARCH \
	--ndk-api $PROJECT_NDK_API
