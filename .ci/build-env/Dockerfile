FROM eclipse-temurin:21-jdk-noble

##############################
# Preinstalling minimal required packages

RUN apt-get update \
   && apt-get install -y --no-install-recommends \
   ca-certificates \
   curl \
   unzip \
   wget \
   && apt -y autoremove \
   && apt -y clean \
   && rm -rf /var/lib/apt/lists/*

##############################
# Install Android SDK Tools

ARG android_sdk_root="/opt/android-sdk"
ENV ANDROID_SDK_ROOT=$android_sdk_root
ENV ANDROIDSDK=$ANDROID_SDK_ROOT

ARG android_sdk_platform_version="35"
ENV ANDROID_SDK_PLATFORM_VERSION=$android_sdk_platform_version
ENV ANDROIDAPI=$ANDROID_SDK_PLATFORM_VERSION

ARG android_sdk_cmdline_tools_version="11076708"
ENV ANDROID_SDK_CMDLINE_TOOLS_VERSION=$android_sdk_cmdline_tools_version

RUN SDK_TOOLS_URL="https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_CMDLINE_TOOLS_VERSION}_latest.zip" \
   && mkdir -p $ANDROID_SDK_ROOT/cmdline-tools \
   && mkdir $ANDROID_SDK_ROOT/platforms \
   && mkdir $ANDROID_SDK_ROOT/ndk \
   && wget --no-check-certificate -O /tmp/cmdline-tools.zip -t 5 "$SDK_TOOLS_URL" \
   && unzip -q /tmp/cmdline-tools.zip -d $ANDROID_SDK_ROOT/cmdline-tools \
   && rm /tmp/cmdline-tools.zip \
   && mv $ANDROID_SDK_ROOT/cmdline-tools/cmdline-tools $ANDROID_SDK_ROOT/cmdline-tools/latest

ARG cmdline_tools_root="$android_sdk_root/cmdline-tools/latest/bin"
ARG android_sdk_build_tools_version="35.0.0"

##############################
# Install Android NDK

# r29
ARG android_ndk_version="29.0.14206865"
ENV ANDROID_NDK_VERSION=$android_ndk_version

ARG android_ndk_root="/opt/android-sdk/ndk/${android_ndk_version}"
ENV ANDROID_NDK_ROOT=$android_ndk_root
ENV ANDROIDNDK=$ANDROID_NDK_ROOT

RUN yes | $cmdline_tools_root/sdkmanager \
   "platform-tools" \
   "build-tools;${android_sdk_build_tools_version}" \
   "platforms;android-${android_sdk_platform_version}" \
   "ndk;${android_ndk_version}"

##############################
# Install requirements for compiling

RUN apt-get update \
   && apt-get install -y --no-install-recommends \
   autoconf \
   automake \
   build-essential \
   binutils \
   ccache \
   cmake \
   gettext \
   git \
   libgcc-s1 \
   libstdc++6 \
   lbzip2 \
   libffi-dev \
   libltdl-dev \
   libssl-dev \
   libtool \
   llvm \
   lld \
   make \
   patch \
   pkg-config \
   sudo \
   unzip \
   wget \
   zip \
   zlib1g-dev \
   && apt -y autoremove \
   && apt -y clean \
   && rm -rf /var/lib/apt/lists/*

##############################
# Install Rust toolchain (required by pydantic-core and other Rust extensions)

ARG rustup_toolchain="stable"
ENV RUSTUP_HOME=/opt/rustup
ENV CARGO_HOME=/opt/cargo
ENV RUSTUP_TOOLCHAIN=${rustup_toolchain}
ENV PATH="${PATH}:${CARGO_HOME}/bin"

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --profile minimal --default-toolchain "${rustup_toolchain}" \
   && "${CARGO_HOME}/bin/rustup" toolchain install "${rustup_toolchain}" \
   && "${CARGO_HOME}/bin/rustup" default "${rustup_toolchain}" \
   && "${CARGO_HOME}/bin/rustup" target add \
   aarch64-linux-android \
   armv7-linux-androideabi \
   i686-linux-android \
   x86_64-linux-android \
   && TOOLCHAIN_SYSROOT="$(rustc --print sysroot)" \
   && ln -sf "${TOOLCHAIN_SYSROOT}/bin/cargo" /usr/local/bin/cargo \
   && ln -sf "${TOOLCHAIN_SYSROOT}/bin/rustc" /usr/local/bin/rustc \
   && rustc --version \
   && cargo --version

##############################
# Install python & python-for-android

ARG p4a_tarball_url=https://github.com/kivy/python-for-android/tarball/develop

ENV P4A_ROOT=/opt/p4a

RUN wget $p4a_tarball_url -O p4a.tgz \
   && mkdir $P4A_ROOT \
   && tar -xz --strip-components=1 -f p4a.tgz -C $P4A_ROOT \
   && rm p4a.tgz

ARG python_version="3.13.12"
ENV PROJECT_PYTHON_VERSION=$python_version

RUN apt-get update \
   && apt-get install -y software-properties-common \
   && add-apt-repository ppa:deadsnakes/ppa \
   && apt-get update \
   && apt-get install -y python3.13 python3.13-dev python3.13-venv \
   && apt -y autoremove \
   && apt -y clean \
   && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1

ENV VIRTUAL_ENV=$P4A_ROOT/.venv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
   PIP_ROOT_USER_ACTION=ignore \
   PIP_FLAGS="--upgrade --no-cache --break-system-packages --ignore-installed"

# starting from here python3 is from virtual environment -->

# Why wheel==0.45.1?
# See https://discuss.python.org/t/upcoming-changes-in-the-pypa-wheel-project/85967/22
RUN python3 -m pip install $PIP_FLAGS setuptools "wheel==0.45.1" \
   && python3 -m pip install $PIP_FLAGS Cython \
   && python3 -m pip install $PIP_FLAGS --editable $P4A_ROOT

##############################
# Configure the environment

# Silences "stty: 'standard input': Inappropriate ioctl for device"
RUN printf '#!/bin/sh\nexit 0\n' > /usr/local/bin/stty \
   && chmod +x /usr/local/bin/stty

ENV PATH="\
${ANDROID_NDK_ROOT}:\
${cmdline_tools_root}:\
$ANDROID_SDK_ROOT/platform-tools:\
$ANDROID_SDK_ROOT/platform-tools/bin:\
$PATH"

ONBUILD RUN \
   export ANDROID_NDK_MAJOR_VERSION=$(echo $ANDROID_NDK_VERSION | cut -d. -f1)
