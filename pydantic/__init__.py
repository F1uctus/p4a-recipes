from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class PydanticRecipe(CompiledComponentsPythonRecipe):
    version = "2.12.5"
    url = "https://pypi.python.org/packages/source/p/pydantic/pydantic-{version}.tar.gz"
    site_packages_name = "pydantic"
    depends = [
        "setuptools",
        "cython",
        "devtools",
        "email-validator",
        "typing-extensions",
        "python-dotenv",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = PydanticRecipe()
