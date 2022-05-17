from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe


class ThincRecipe(CppCompiledComponentsPythonRecipe):
    version = "master"
    url = (
        "https://github.com/explosion/thinc/archive/master.tar.gz"
        if version == "master"
        else "https://pypi.python.org/packages/source/t/thinc/thinc-{version}.tar.gz"
    )
    site_packages_name = "thinc"
    depends = [
        "murmurhash",
        "cymem",
        "preshed",
        "blis",
        "srsly",
        "wasabi",
        "catalogue",
        "ml_datasets",
        "pydantic",
        "numpy",
        "typing_extensions",
        "contextvars",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        if self.need_stl_shared:
            # thinc compile flags does not honor the standard flags:
            # `CPPFLAGS` and `LDLIBS`, so we put in `CFLAGS` and `LDFLAGS` to
            # correctly link with the `c++_shared` library
            env["CFLAGS"] += f" -I{self.stl_include_dir}"
            env["CFLAGS"] += " -frtti -fexceptions"

            env["LDFLAGS"] += f" -L{self.get_stl_lib_dir(arch)}"
            env["LDFLAGS"] += f" -l{self.stl_lib_name}"

        cli = env["CC"].split()[0]
        ccache_bin = cli if "ccache" in cli else ""

        env["BLIS_COMPILER"] = " ".join(
            [
                ccache_bin,
                arch.get_clang_exe(with_target=True),
            ]
        )

        return env


recipe = ThincRecipe()
