from pythonforandroid.recipe import CompiledComponentsPythonRecipe, Recipe


class PreshedRecipe(CompiledComponentsPythonRecipe):
    version = "3.0.12"
    url = "https://files.pythonhosted.org/packages/source/p/preshed/preshed-{version}.tar.gz"
    site_packages_name = "preshed"
    depends = [
        "setuptools",
        "cython",
        "cymem",
        "murmurhash",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        if arch is None:
            return env

        # Make sure Cython can find .pxd files from dependencies when building
        # via hostpython (e.g. `from cymem.cymem cimport Pool`).
        dep_build_dirs = [
            Recipe.get_recipe("cymem", self.ctx).get_build_dir(arch.arch),
            Recipe.get_recipe("murmurhash", self.ctx).get_build_dir(arch.arch),
        ]
        existing = env.get("CYTHON_INCLUDE_PATH")
        env["CYTHON_INCLUDE_PATH"] = ":".join(
            ([existing] if existing else []) + dep_build_dirs
        )
        return env


recipe = PreshedRecipe()
