from pythonforandroid.recipe import PythonRecipe


class RequestsRecipe(PythonRecipe):
    version = "2.32.5"
    url = "https://pypi.python.org/packages/source/r/requests/requests-{version}.tar.gz"
    site_packages_name = "requests"
    depends = [
        "setuptools",
        "charset_normalizer",
        "chardet",
        "idna",
        "urllib3",
        "certifi",
    ]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True


recipe = RequestsRecipe()
