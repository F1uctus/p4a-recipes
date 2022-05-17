from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class ThincRecipe(CompiledComponentsPythonRecipe):
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
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = ThincRecipe()
