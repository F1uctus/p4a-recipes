from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class ThincRecipe(CompiledComponentsPythonRecipe):
    version = "master"
    url = (
        "https://github.com/explosion/thinc/archive/90631684f8e4448fb5894cc8ab748a68939f2654.tar.gz"
        if version == "master"
        else "https://pypi.python.org/packages/source/t/thinc/thinc-{version}.tar.gz"
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
        "ml_datasets",
        # Third-party dependencies
        "pydantic",
        "numpy",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env["CXXFLAGS"] = env["CFLAGS"] + " -frtti -fexceptions"

        if with_flags_in_cc:
            env["CXX"] += " -frtti -fexceptions"

        env["LDFLAGS"] += " -L{}".format(self.get_stl_lib_dir(arch))
        env["LIBS"] = env.get("LIBS", "") + " -l{}".format(self.stl_lib_name)
        return env

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        self.install_stl_lib(arch)


recipe = ThincRecipe()
