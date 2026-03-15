from pythonforandroid.recipe import RustCompiledComponentsRecipe
from pythonforandroid.toolchain import current_directory
from os.path import join


class PydanticcoreRecipe(RustCompiledComponentsRecipe):
    version = "2.42.0"
    url = "https://files.pythonhosted.org/packages/source/p/pydantic-core/pydantic_core-{version}.tar.gz"
    site_packages_name = "pydantic_core"
    depends = ["python3", "setuptools", "hostpython3"]
    hostpython_prerequisites = ["maturin>=1.5.0"]


recipe = PydanticcoreRecipe()
