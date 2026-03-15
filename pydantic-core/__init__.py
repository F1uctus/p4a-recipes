from pythonforandroid.recipe import RustCompiledComponentsRecipe
from pythonforandroid.toolchain import current_directory
from os.path import join


class PydanticcoreRecipe(RustCompiledComponentsRecipe):
    version = "2.42.0"
    url = "https://github.com/pydantic/pydantic-core/archive/refs/tags/v{version}.zip"
    site_packages_name = "pydantic_core"
    depends = ["python3", "setuptools", "hostpython3"]
    hostpython_prerequisites = ["maturin>=1.5.0"]


recipe = PydanticcoreRecipe()
