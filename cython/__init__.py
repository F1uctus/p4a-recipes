from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class CythonRecipe(CompiledComponentsPythonRecipe):

    version = "3.2.4"
    url = "https://github.com/cython/cython/archive/{version}.tar.gz"
    site_packages_name = "cython"
    depends = ["setuptools"]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_hostrecipe_env(self, arch=None):
        env = super().get_hostrecipe_env(arch)
        env["CC"] = "/usr/bin/ccache gcc"
        return env


recipe = CythonRecipe()
