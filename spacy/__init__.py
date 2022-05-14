from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe


class SpacyRecipe(CppCompiledComponentsPythonRecipe):
    version = "3.2.2"
    url = "https://pypi.python.org/packages/source/s/spacy/spacy-{version}.tar.gz"
    site_packages_name = "spacy"
    depends = [
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
        "numpy",
        "requests",
        "urllib3",
        "tqdm",
        "pydantic",

        # Required for Russian language
        "pymorphy2",
        "pymorphy2_dicts_ru",
        "DAWG-Python",
        "appdirs",
        
        "pyparsing",
        "jinja2",
        "langcodes",
        "setuptools",
        "packaging",
        "typing_extensions",
    ]
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=False):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        if self.need_stl_shared:
            # spacy compile flags does not honor the standard flags:
            # `CPPFLAGS` and `LDLIBS`, so we put in `CFLAGS` and `LDFLAGS` to
            # correctly link with the `c++_shared` library
            env["CFLAGS"] += f" -I{self.stl_include_dir}"
            env["CFLAGS"] += " -frtti -fexceptions"

            env["LDFLAGS"] += f" -L{self.get_stl_lib_dir(arch)}"
            env["LDFLAGS"] += f" -l{self.stl_lib_name}"
        return env


recipe = SpacyRecipe()
