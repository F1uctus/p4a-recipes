from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.logger import shprint, info
from pythonforandroid.util import current_directory
from multiprocessing import cpu_count
from os.path import join, abspath, dirname
import glob
import sh


class NumpyRecipe(CompiledComponentsPythonRecipe):

    version = '1.18.1'
    url = 'https://pypi.python.org/packages/source/n/numpy/numpy-{version}.zip'
    site_packages_name = 'numpy'
    depends = ['setuptools', 'cython']
    install_in_hostpython = True
    call_hostpython_via_targetpython = False

    patches = [
        join(dirname(abspath(__file__)), 'patches', 'hostnumpy-xlocale.patch'),
        join(dirname(abspath(__file__)), 'patches', 'remove-default-paths.patch'),
        join(dirname(abspath(__file__)), 'patches', 'add_libm_explicitly_to_build.patch'),
        join(dirname(abspath(__file__)), 'patches', 'compiler_cxx_fix.patch'),
        join(dirname(abspath(__file__)), 'patches', 'fix_empty_doc_error_on_import.patch'),
    ]

    def _build_compiled_components(self, arch):
        info('Building compiled components in {}'.format(self.name))

        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            hostpython = sh.Command(self.real_hostpython_location)
            if self.install_in_hostpython:
                shprint(hostpython, 'setup.py', 'clean', '--all', '--force', _env=env)
            hostpython = sh.Command(self.hostpython_location)
            shprint(hostpython, 'setup.py', self.build_cmd, '-v',
                    _env=env, *self.setup_extra_args)
            build_dir = glob.glob('build/lib.*')[0]
            shprint(sh.find, build_dir, '-name', '"*.o"', '-exec',
                    env['STRIP'], '{}', ';', _env=env)

    def _rebuild_compiled_components(self, arch, env):
        info('Rebuilding compiled components in {}'.format(self.name))

        hostpython = sh.Command(self.real_hostpython_location)
        shprint(hostpython, 'setup.py', 'clean', '--all', '--force', _env=env)
        shprint(hostpython, 'setup.py', self.build_cmd, '-v', _env=env,
                *self.setup_extra_args)

    def build_compiled_components(self, arch):
        self.setup_extra_args = ['-j', str(cpu_count())]
        self._build_compiled_components(arch)
        self.setup_extra_args = []

    def rebuild_compiled_components(self, arch, env):
        self.setup_extra_args = ['-j', str(cpu_count())]
        self._rebuild_compiled_components(arch, env)
        self.setup_extra_args = []


recipe = NumpyRecipe()
