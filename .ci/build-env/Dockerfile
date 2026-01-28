FROM eclipse-temurin:21-jre-ubi9-minimal

ENV DEBIAN_FRONTEND=noninteractive

##############################
# Preinstalling minimal required packages

RUN microdnf install -y \
    unzip \
    wget \
 && microdnf clean all

##############################
# Install Android SDK Tools

ARG android_sdk_root="/opt/android-sdk"
ENV ANDROID_SDK_ROOT=$android_sdk_root
ENV ANDROIDSDK=$ANDROID_SDK_ROOT

ARG android_sdk_platform_version="36"
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

RUN echo y | $cmdline_tools_root/sdkmanager \
                "platform-tools" \
                "build-tools;${android_sdk_build_tools_version}" \
                "platforms;android-${android_sdk_platform_version}" \
                "ndk;${android_ndk_version}"

##############################
# Install requirements for compiling

RUN microdnf install -y \
    autoconf \
    automake \
    ccache \
    cmake \
    gcc \
    gcc-c++ \
    gettext \
    git \
    libffi-devel \
    libtool \
    make \
    openssl-devel \
    patch \
    pkgconf-pkg-config \
    python3 \
    python3-devel \
    python3-pip \
    sudo \
    unzip \
    wget \
    zip \
    zlib-devel \
 && microdnf clean all

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

ENV PATH="\
${ANDROID_NDK_ROOT}\
${cmdline_tools_root}:\
$ANDROID_SDK_ROOT/platform-tools:\
$ANDROID_SDK_ROOT/platform-tools/bin:\
$PATH"

ONBUILD RUN export ANDROID_NDK_MAJOR_VERSION=$(echo $ANDROID_NDK_VERSION | cut -d. -f1)
