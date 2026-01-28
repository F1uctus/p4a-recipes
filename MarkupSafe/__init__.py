from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class MarkupSafeRecipe(CompiledComponentsPythonRecipe):
    version = "3.0.3"
    url = "https://files.pythonhosted.org/packages/7e/99/7690b6d4034fffd95959cbe0c02de8deb3098cc577c67bb6a24fe5d7caa7/markupsafe-3.0.3.tar.gz"
    depends = [
        "setuptools",
        "cython",
        "pyparsing",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = MarkupSafeRecipe()
