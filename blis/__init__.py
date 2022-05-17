from pythonforandroid.archs import (
    ArchAarch_64,
    Archx86_64,
)
from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class BlisRecipe(CompiledComponentsPythonRecipe):
    version = "0.9.0"
    url = "https://github.com/explosion/cython-blis/archive/refs/tags/v{version}.tar.gz"
    depends = ["setuptools", "cython", "numpy"]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)

        # see https://github.com/flame/blis/blob/master/config_registry
        if isinstance(arch, ArchAarch_64):
            env["BLIS_ARCH"] = "arm64"
        elif isinstance(arch, Archx86_64):
            env["BLIS_ARCH"] = "x86_64"
        else:
            env["BLIS_ARCH"] = "generic"

        cli = env["CC"].split()[0]
        ccache_bin = cli if "ccache" in cli else ""

        env["BLIS_COMPILER"] = " ".join(
            [
                ccache_bin,
                arch.get_clang_exe(with_target=True),
            ]
        )

        return env


recipe = BlisRecipe()
