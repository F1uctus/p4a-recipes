from pythonforandroid.recipes.hostpython3 import HostPython3Recipe


class MyHostPython3Recipe(HostPython3Recipe):
    version = "3.13.12"
    url = "https://github.com/python/cpython/archive/refs/tags/v{version}.tar.gz"


recipe = MyHostPython3Recipe()
