from pythonforandroid.recipe import CompiledComponentsPythonRecipe, Recipe


class SpacyRecipe(CompiledComponentsPythonRecipe):
    version = "3.8.11"
    url = "https://files.pythonhosted.org/packages/source/s/spacy/spacy-{version}.tar.gz"
    site_packages_name = "spacy"
    depends = [
        "setuptools",
        "cython",
        # Explosion-provided dependencies
        "spacy-legacy",
        "spacy-loggers",
        "cymem",
        "click",
        "preshed",
        "thinc",
        "blis",
        "markupsafe",
        "ml_datasets",
        "murmurhash",
        "wasabi",
        "srsly",
        "catalogue",
        "typer",
        "pathy",
        # Third party dependencies
        "numpy",
        "requests",
        "urllib3",
        "tqdm",
        "pydantic",
        "jinja2",
        "langcodes",
        # Official Python utilities
        "packaging",
        # Required for Russian language
        "pymorphy2",
        "pymorphy2_dicts_ru",
        "DAWG-Python",
        "appdirs",
        "pyparsing",
    ]
    call_hostpython_via_targetpython = False

    def get_hostrecipe_env(self, arch=None):
        env = super().get_hostrecipe_env(arch)
        if arch is None:
            return env

        dep_build_dirs = [
            Recipe.get_recipe("cymem", self.ctx).get_build_dir(arch.arch),
            Recipe.get_recipe("preshed", self.ctx).get_build_dir(arch.arch),
            Recipe.get_recipe("murmurhash", self.ctx).get_build_dir(arch.arch),
        ]

        for key in ("CYTHON_INCLUDE_PATH", "PYTHONPATH"):
            existing = env.get(key)
            env[key] = ":".join(([existing] if existing else []) + dep_build_dirs)

        return env

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env["CXXFLAGS"] = env["CFLAGS"] + " -frtti -fexceptions"

        if arch is not None:
            # Ensure Cython can resolve .pxd files from compiled deps when
            # cythonizing via hostpython.
            dep_build_dirs = [
                Recipe.get_recipe("cymem", self.ctx).get_build_dir(arch.arch),
                Recipe.get_recipe("preshed", self.ctx).get_build_dir(arch.arch),
                Recipe.get_recipe("murmurhash", self.ctx).get_build_dir(arch.arch),
            ]
            existing = env.get("CYTHON_INCLUDE_PATH")
            env["CYTHON_INCLUDE_PATH"] = ":".join(
                ([existing] if existing else []) + dep_build_dirs
            )
            existing = env.get("PYTHONPATH")
            env["PYTHONPATH"] = ":".join(([existing] if existing else []) + dep_build_dirs)

        if with_flags_in_cc:
            env["CXX"] += " -frtti -fexceptions"

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


recipe = SpacyRecipe()
