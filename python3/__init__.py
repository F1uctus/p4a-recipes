from pythonforandroid.recipes.python3 import Python3Recipe

class MyPython3Recipe(Python3Recipe):
    version = "3.13.12"
    url = "https://github.com/python/cpython/archive/refs/tags/v{version}.tar.gz"

recipe = MyPython3Recipe()