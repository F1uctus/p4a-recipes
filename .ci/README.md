### Usage example

Building spaCy for arm-v8a using python-for-android:

```console
docker build ./build-env --tag p4a/build-env
docker build ./bundle    --tag p4a/spacy
docker run -v p4a-build-cache:/root/.local/share p4a/spacy
```

Then for the target platform you can grab:
- `python-bundle`;
- `modules`;
- `site-packages`;
- `stdlib.zip`;
- etc.

from the `p4a-build-cache` docker volume.

*You can customize the build with Docker's `--build-arg`s:*

For the `build-env` image:
- "p4a_tarball_url=https://github.com/kivy/python-for-android/tarball/develop"
- "android_sdk_platform_version=27";
- "android_sdk_cmdline_tools_version=8092744"
  (taken from https://dl.google.com/android/repository/commandlinetools-linux/...);
- "android_sdk_build_tools_version=32.0.0";
- "android_ndk_version=23.1.7779620";

For the `bundle` image:
- The p4a recipe set to use ("recipe_tarball_url=https://github.com/F1uctus/p4a-recipes/tarball/4c487202b2a2ef5d18f8bfdd9b7c50a946e52865")
- The python version (e.g. "python_version=3.10.4");
- The target packages to build (comma-separated, "requirements=spacy,etc");
- The minimum supported Android SDK version ("min_android_api=24").

...see other build options in the contained `Dockerfile`s.
