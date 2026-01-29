from pythonforandroid.recipe import CompiledComponentsPythonRecipe

from ..shared import extend_env_with_recipe_build_dirs


class SpacyRecipe(CompiledComponentsPythonRecipe):
    version = "3.8.11"
    url = (
        "https://files.pythonhosted.org/packages/source/s/spacy/spacy-{version}.tar.gz"
    )
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
        return extend_env_with_recipe_build_dirs(
            env,
            ctx=self.ctx,
            arch=arch,
            recipe_names=("cymem", "preshed", "murmurhash", "thinc"),
        )

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env["CXXFLAGS"] = env["CFLAGS"] + " -frtti -fexceptions"

        extend_env_with_recipe_build_dirs(
            env,
            ctx=self.ctx,
            arch=arch,
            recipe_names=("cymem", "preshed", "murmurhash", "thinc"),
        )

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
