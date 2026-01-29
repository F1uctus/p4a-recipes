from pythonforandroid.recipe import CompiledComponentsPythonRecipe

from shared import extend_env_with_recipe_build_dirs


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

    def get_hostrecipe_env(self, arch=None):
        env = super().get_hostrecipe_env(arch)
        return extend_env_with_recipe_build_dirs(
            env,
            ctx=self.ctx,
            arch=arch,
            recipe_names=("cymem", "murmurhash"),
        )

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        extend_env_with_recipe_build_dirs(
            env,
            ctx=self.ctx,
            arch=arch,
            recipe_names=("cymem", "murmurhash"),
        )
        return env


recipe = PreshedRecipe()
