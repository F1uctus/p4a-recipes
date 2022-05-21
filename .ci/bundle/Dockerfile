FROM p4a/build-env

##############################
# Download the recipe set

ENV WORKDIR /root/bundle
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR

ARG recipe_tarball_url=https://github.com/F1uctus/p4a-recipes/tarball/4c487202b2a2ef5d18f8bfdd9b7c50a946e52865

RUN wget $recipe_tarball_url -O p4a-recipes.tgz \
 && mkdir local_recipes \
 && tar -xz --strip-components=1 -f p4a-recipes.tgz -C local_recipes \
 && rm p4a-recipes.tgz

RUN mkdir src && > src/main.py

##############################
# Install project build dependencies

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
	ant \
	libc6-dev \
	libgdbm-dev \
	libncursesw5-dev \
	libsqlite3-dev \
	lld \
	openssl \
	python3-setuptools \
	python3-smbus \
	tk-dev \
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

ARG bootstrap="service_only"
ENV PROJECT_BOOTSTRAP=$bootstrap

ARG python_version="3.10.4"
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
	--private $WORKDIR/src \
	--name "bundle" \
	--version "1.0" \
	--package "org.p4a.bundle" \
	--bootstrap "$PROJECT_BOOTSTRAP" \
	--requirements "${PROJECT_PYTHON_REQUIREMENTS}${PROJECT_REQUIREMENTS}" \
	--blacklist-requirements android \
	--local-recipes $WORKDIR/local_recipes \
	--arch $PROJECT_ARCH \
	--ndk-api $PROJECT_NDK_API
