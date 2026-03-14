from pythonforandroid.recipe import PythonRecipe


class PydanticRecipe(PythonRecipe):
    version = "2.13.0b2"
    url = "https://github.com/pydantic/pydantic/archive/refs/tags/v{version}.zip"
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
