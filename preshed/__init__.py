from pythonforandroid.recipe import CompiledComponentsPythonRecipe


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

    def _extend_env(self, env, arch):
        if arch is None:
            return env
        dep_build_dirs = list(
            dict.fromkeys(
                [
                    self.get_recipe(name, self.ctx).get_build_dir(arch.arch)
                    for name in ("cymem", "murmurhash")
                ]
            )
        )
        for key in ("CYTHON_INCLUDE_PATH", "PYTHONPATH"):
            env[key] = ":".join(dep_build_dirs + ([x] if (x := env.get(key)) else []))
        return env

    def get_hostrecipe_env(self, arch=None):
        env = super().get_hostrecipe_env(arch)
        return self._extend_env(env, arch)

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        return self._extend_env(env, arch)


recipe = PreshedRecipe()
