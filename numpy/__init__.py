from pythonforandroid.recipe import Recipe, MesonRecipe
from pythonforandroid.util import current_directory, ensure_dir
from pythonforandroid.logger import shprint
from os.path import join, isdir
import shutil
import sh

NUMPY_NDK_MESSAGE = (
    "In order to build numpy, you must set minimum ndk api (minapi) to `24`.\n"
)


class NumpyRecipe(MesonRecipe):
    version = "v2.3.0"
    url = "https://github.com/numpy/numpy"
    hostpython_prerequisites = [
        "Cython>=3.0.6",
        "numpy",
    ]  # meson does not detects venv's cython
    extra_build_args = ["-Csetup-args=-Dblas=none", "-Csetup-args=-Dlapack=none"]
    need_stl_shared = True
    min_ndk_api_support = 24

    def download_file(self, url, target, cwd=None):
        if cwd:
            target = join(cwd, target)
        if not isdir(target):
            ensure_dir(target)
            shprint(sh.git, 'clone', '--recursive', url, target)
        with current_directory(target):
            shprint(sh.git, 'fetch', '--tags', '--force', '--depth', '1')
            shprint(sh.git, 'checkout', self.version)
            shprint(sh.git, 'submodule', 'update', '--recursive', '--init', '--depth', '1')
        return target

    def get_recipe_meson_options(self, arch):
        options = super().get_recipe_meson_options(arch)
        # Custom python is required, so that meson
        # gets libs and config files properly
        options["binaries"]["python"] = self.ctx.python_recipe.python_exe
        options["binaries"]["python3"] = self.ctx.python_recipe.python_exe
        options["properties"]["longdouble_format"] = (
            "IEEE_DOUBLE_LE" if arch.arch in ["armeabi-v7a", "x86"] else "IEEE_QUAD_LE"
        )
        return options

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)

        # _PYTHON_HOST_PLATFORM declares that we're cross-compiling
        # and avoids issues when building on macOS for Android targets.
        env["_PYTHON_HOST_PLATFORM"] = arch.command_prefix

        # NPY_DISABLE_SVML=1 allows numpy to build for non-AVX512 CPUs
        # See: https://github.com/numpy/numpy/issues/21196
        env["NPY_DISABLE_SVML"] = "1"
        env["TARGET_PYTHON_EXE"] = join(
            Recipe.get_recipe("python3", self.ctx).get_build_dir(arch.arch),
            "android-build",
            "python",
        )
        return env

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        # Fix for NumPy 2.x docstring optimization issue on Android.
        # This prevents "TypeError: argument docstring of add_docstring should be a str"
        # when docstrings are stripped by the bytecode optimizer (-OO).
        overrides_py = join(self.get_build_dir(arch.arch), 'numpy', '_core', 'overrides.py')

        # Note: If numpy 2.x is used, the file is in _core. In 1.x it was in core.
        if not isdir(join(self.get_build_dir(arch.arch), 'numpy', '_core')):
            overrides_py = join(self.get_build_dir(arch.arch), 'numpy', 'core', 'overrides.py')

        self.logger.info(f"Patching NumPy overrides at {overrides_py}")
        with open(overrides_py, 'r') as f:
            content = f.read()

        # Wrap add_docstring calls in existence checks
        content = content.replace(
            'add_docstring(implementation, dispatcher.__doc__)',
            'if isinstance(dispatcher.__doc__, str): add_docstring(implementation, dispatcher.__doc__)'
        )
        content = content.replace(
            'add_docstring(implementation, doc)',
            'if isinstance(doc, str): add_docstring(implementation, doc)'
        )

        with open(overrides_py, 'w') as f:
            f.write(content)

    def build_arch(self, arch):
        super().build_arch(arch)
        self.restore_hostpython_prerequisites(["cython"])

    def get_hostrecipe_env(self, arch=None):
        env = super().get_hostrecipe_env(arch=arch)
        env["RANLIB"] = shutil.which("ranlib")
        return env


recipe = NumpyRecipe()
