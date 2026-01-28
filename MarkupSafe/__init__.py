from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class MarkupSafeRecipe(CompiledComponentsPythonRecipe):
    version = "3.0.3"
    url = "https://pypi.python.org/packages/source/M/MarkupSafe/MarkupSafe-{version}.tar.gz"
    depends = [
        "setuptools",
        "cython",
        "pyparsing",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = MarkupSafeRecipe()
