ARG BASE_IMAGE=p4a/build-env
FROM ${BASE_IMAGE}

ENV WORKDIR=/root/bundle
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR

##############################
# Download the recipe set

ARG recipe_tarball_url=https://github.com/F1uctus/p4a-recipes/tarball/main

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
# Build the project

VOLUME /root/.local/share
VOLUME /root/.ccache

ENV PROJECT_PYTHON_REQUIREMENTS="hostpython3,python3,"

ARG requirements="spacy==3.8.11"
ENV PROJECT_REQUIREMENTS=$requirements

ARG arch="arm64-v8a"
ENV PROJECT_ARCH=$arch

ARG min_android_api="24"
ENV PROJECT_NDK_API=$min_android_api

ENTRYPOINT p4a aar \
	--release \
	--private $WORKDIR/src \
	--name bundle \
	--dist_name bundle \
	--version 1.0 \
	--package org.p4a.bundle \
	--bootstrap service_library \
	--requirements "${PROJECT_PYTHON_REQUIREMENTS}${PROJECT_REQUIREMENTS}" \
	--no-optimize-python \
	--blacklist-requirements android,sdl2 \
	--local-recipes $WORKDIR/local_recipes \
	--arch $PROJECT_ARCH \
	--ndk-api $PROJECT_NDK_API \
	--debug
