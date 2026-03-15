from pythonforandroid.recipe import RustCompiledComponentsRecipe
from pythonforandroid.toolchain import current_directory
from os.path import join


class PydanticcoreRecipe(RustCompiledComponentsRecipe):
    version = "2.42.0"
    url = "https://github.com/pydantic/pydantic/archive/refs/tags/v2.13.0b2.zip"
    site_packages_name = "pydantic_core"
    depends = ["python3", "setuptools"]

    def build_arch(self, arch):
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(join(build_dir, "pydantic-core")):
            super().build_arch(arch)


recipe = PydanticcoreRecipe()
