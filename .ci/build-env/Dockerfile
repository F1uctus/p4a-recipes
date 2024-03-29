FROM eclipse-temurin:17

ENV DEBIAN_FRONTEND=noninteractive

##############################
# Preinstalling minimal required packages

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    unzip \
    wget \
 && apt -y autoremove \
 && apt -y clean \
 && rm -rf /var/lib/apt/lists/*

##############################
# Install Android SDK Tools

ARG android_sdk_root="/opt/android-sdk"
ENV ANDROID_SDK_ROOT=$android_sdk_root
ENV ANDROIDSDK $ANDROID_SDK_ROOT

ARG android_sdk_platform_version="31"
ENV ANDROID_SDK_PLATFORM_VERSION=$android_sdk_platform_version
ENV ANDROIDAPI $ANDROID_SDK_PLATFORM_VERSION

ARG android_sdk_cmdline_tools_version="8092744"
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
ARG android_sdk_build_tools_version="33.0.0"

RUN echo y | $cmdline_tools_root/sdkmanager \
                "tools" "platform-tools" \
                "build-tools;${android_sdk_build_tools_version}" \
 && $cmdline_tools_root/sdkmanager --uninstall emulator

RUN echo y | $cmdline_tools_root/sdkmanager "platforms;android-${android_sdk_platform_version}"

##############################
# Install Android NDK

# 23.1.7779620 => r23b
# 23.2.8568313 => r23c
ARG android_ndk_version="23.2.8568313" 
ENV ANDROID_NDK_VERSION=$android_ndk_version


ARG android_ndk_root="/opt/android-sdk/ndk/${android_ndk_version}"
ENV ANDROID_NDK_ROOT=$android_ndk_root
ENV ANDROIDNDK=$ANDROID_NDK_ROOT

RUN echo y | $cmdline_tools_root/sdkmanager "ndk;${ANDROID_NDK_VERSION}"

##############################
# Install requirements for compiling

RUN dpkg --add-architecture i386

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    autoconf \
    automake \
    autopoint \
    build-essential \
    ccache \
    cmake \
    gettext \
    git \
    lbzip2 \
    libffi-dev \
    libgtk2.0-0:i386 \
    libidn11-dev:i386 \
    libltdl-dev \
    libncurses5:i386 \
    libssl-dev \
    libstdc++6:i386 \
    libtool \
    patch \
    pkg-config \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    sudo \
    zip \
    zlib1g-dev \
    zlib1g:i386 \
 && apt -y autoremove \
 && apt -y clean \
 && rm -rf /var/lib/apt/lists/*

##############################
# Install python-for-android

ARG p4a_tarball_url=https://github.com/kivy/python-for-android/tarball/develop

RUN wget $p4a_tarball_url -O p4a.tgz \
 && mkdir /opt/p4a \
 && tar -xz --strip-components=1 -f p4a.tgz -C /opt/p4a \
 && rm p4a.tgz

RUN pip install Cython \
 && pip install -e /opt/p4a \
 && rm -rf ~/.cache/

##############################
# Configure the environment

ENV PATH "\
${ANDROID_NDK_ROOT}\
${cmdline_tools_root}:\
$ANDROID_SDK_ROOT/tools:\
$ANDROID_SDK_ROOT/tools/bin:\
$ANDROID_SDK_ROOT/platform-tools:\
$ANDROID_SDK_ROOT/platform-tools/bin:\
$PATH"

ONBUILD RUN export ANDROID_NDK_MAJOR_VERSION=$(echo $ANDROID_NDK_VERSION | cut -d. -f1)
