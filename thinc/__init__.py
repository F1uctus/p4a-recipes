from pythonforandroid.recipe import CompiledComponentsPythonRecipe

from shared import extend_env_with_recipe_build_dirs


class ThincRecipe(CompiledComponentsPythonRecipe):
    version = "8.3.10"
    url = (
        "https://github.com/explosion/thinc/archive/90631684f8e4448fb5894cc8ab748a68939f2654.tar.gz"
        if version == "master"
        else "https://files.pythonhosted.org/packages/source/t/thinc/thinc-{version}.tar.gz"
    )
    site_packages_name = "thinc"
    depends = [
        "setuptools",
        "cython",
        # Explosion-provided dependencies
        "murmurhash",
        "cymem",
        "preshed",
        "blis",
        "srsly",
        "wasabi",
        "catalogue",
        "confection",
        "ml_datasets",
        # Third-party dependencies
        "pydantic",
        "numpy",
        "packaging",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_hostrecipe_env(self, arch=None):
        env = super().get_hostrecipe_env(arch)
        return extend_env_with_recipe_build_dirs(
            env,
            ctx=self.ctx,
            arch=arch,
            recipe_names=("cymem", "murmurhash", "preshed", "blis"),
        )

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env["CXXFLAGS"] = env["CFLAGS"] + " -frtti -fexceptions"

        if with_flags_in_cc:
            env["CXX"] += " -frtti -fexceptions"

        extend_env_with_recipe_build_dirs(
            env,
            ctx=self.ctx,
            arch=arch,
            recipe_names=("cymem", "murmurhash", "preshed", "blis"),
        )

        # Ensure the extension modules *link* against the shared C++ runtime so
        # it ends up in DT_NEEDED (not just copied into the APK).
        stl_link_args = " -L{dir} -Wl,--no-as-needed -l{name} -Wl,--as-needed".format(
            dir=self.get_stl_library(arch),
            name=self.stl_lib_name,
        )
        env["LDFLAGS"] += stl_link_args
        if "LDSHARED" in env:
            env["LDSHARED"] += stl_link_args
        return env

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        self.install_stl_lib(arch)


recipe = ThincRecipe()
