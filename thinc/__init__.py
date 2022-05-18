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
        "setuptools",
        "cython",
        # from requirements
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
    ]
    install_in_hostpython = True


recipe = ThincRecipe()
