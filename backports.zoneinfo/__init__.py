from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class BackportsZoneinfoRecipe(CompiledComponentsPythonRecipe):
    version = "2.4.2"
    url = "https://pypi.python.org/packages/source/b/backports.zoneinfo/backports.zoneinfo-{version}.tar.gz"
    depends = ["setuptools", "cython"]
    call_hostpython_via_targetpython = False


recipe = BackportsZoneinfoRecipe()
