from pythonforandroid.recipe import PythonRecipe


class PydanticRecipe(PythonRecipe):
    version = "2.12.5"
    url = "https://files.pythonhosted.org/packages/source/p/pydantic/pydantic-{version}.tar.gz"
    site_packages_name = "pydantic"
    depends = [
        "setuptools",
        # https://github.com/kivy/python-for-android/blob/develop/pythonforandroid/recipes/pydantic-core/__init__.py
        "pydantic-core",
        # Runtime python deps
        "annotated-types",
        "typing-extensions",
        "typing-inspection",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = PydanticRecipe()
