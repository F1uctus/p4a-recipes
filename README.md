# F1uctus's recipes for python-for-android

**Side-notes**:

- SQLite must be included (do not blacklist `sqlite3`) or Python configure fails.
- MarkupSafe uses a hashed PyPI URL; other recipes use files.pythonhosted.org.
- Recipes expect `get_hostrecipe_env(arch=None)` to avoid missing-arg errors.
- NDK r29 supports up to API 35; set `android_sdk_platform_version=35` to avoid ndk-build aborts.
- NDK r28c is max supported by python-for-android.
- `wheel<0.43` is required in the build env (missing `wheel.cli` breaks installs).
- Bundle `Dockerfile` accepts `BASE_IMAGE` for GHCR build-env reuse.
