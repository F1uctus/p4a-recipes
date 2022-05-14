from pythonforandroid.archs import (
    ArchAarch_64,
)
from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class BlisRecipe(CompiledComponentsPythonRecipe):
    version = "0.7.5"
    url = (
        "https://github.com/explosion/cython-blis/archive/master.tar.gz"
        if (0, 7, 5) <= tuple(map(int, version.split("."))) < (8, 0, 0)
        else "https://github.com/explosion/cython-blis/archive/refs/tags/v{version}.tar.gz"
    )
    depends = ["setuptools", "cython", "numpy"]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    # def prebuild_arch(self, arch):
    #     super().prebuild_arch(arch)
    #
    #     if isinstance(arch, ArchARMv7_a):
    #         with current_directory(self.get_build_dir(arch.arch)):
    #             shutil.copy(
    #                 join(dirname(realpath(__file__)), "linux-cortexa15.jsonl"),
    #                 join(".", "blis", "_src", "make", "linux-cortexa15.jsonl"),
    #             )
    #             shutil.copytree(
    #                 join(dirname(realpath(__file__)), "linux-cortexa15"),
    #                 join(".", "blis", "_src", "include", "linux-cortexa15"),
    #                 dirs_exist_ok=True,
    #             )

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)

        # see https://github.com/flame/blis/blob/master/config_registry
        cflags = ""
        if isinstance(arch, ArchAarch_64):
            # env["BLIS_ARCH"] = "cortexa57"
            cflags = "-no-integrated-as"
        # elif isinstance(arch, Archx86_64):
        #     env["BLIS_ARCH"] = "x86_64"
        # else:
        env["BLIS_ARCH"] = "generic"

        cli = env["CC"].split()[0]
        ccache_bin = cli if "ccache" in cli else ""

        env["BLIS_COMPILER"] = " ".join(
            [
                ccache_bin,
                arch.get_clang_exe(with_target=True),
                cflags,
            ]
        )

        return env


recipe = BlisRecipe()
