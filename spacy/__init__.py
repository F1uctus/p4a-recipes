from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class SpacyRecipe(CompiledComponentsPythonRecipe):
    version = "3.3.0"
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


recipe = SpacyRecipe()
