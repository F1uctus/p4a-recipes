from pythonforandroid.recipe import CompiledComponentsPythonRecipe, Recipe


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

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env["CXXFLAGS"] = env["CFLAGS"] + " -frtti -fexceptions"

        if with_flags_in_cc:
            env["CXX"] += " -frtti -fexceptions"

        if arch is not None:
            # Make sure Cython can find .pxd files from dependencies when building
            # via hostpython (e.g. `cimport blis.cy`).
            dep_build_dirs = [
                Recipe.get_recipe("blis", self.ctx).get_build_dir(arch.arch),
            ]
            existing_cython = env.get("CYTHON_INCLUDE_PATH")
            env["CYTHON_INCLUDE_PATH"] = ":".join(
                dep_build_dirs + ([existing_cython] if existing_cython else [])
            )

            # Some builds ignore CYTHON_INCLUDE_PATH, but Cython always considers
            # sys.path. Ensure dependency source trees are on it.
            existing_py = env.get("PYTHONPATH")
            env["PYTHONPATH"] = ":".join(
                dep_build_dirs + ([existing_py] if existing_py else [])
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
