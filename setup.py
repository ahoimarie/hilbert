from setuptools import setup
import os


def _package_tree(pkgroot):
    path = os.path.dirname(__file__)
    subdirs = [os.path.relpath(i[0], path).replace(os.path.sep, '.')
               for i in os.walk(os.path.join(path, pkgroot))
               if '__init__.py' in i[2]]
    return subdirs


curdir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(curdir, 'README.md')) as f:
    readme = f.read()


with open('requirements.txt') as f:
    require = [x.strip() for x in f.readlines() if not x.startswith('git+')]

setup(
   name='hilbert',
   version='1.0',
   license="GPL-2.0 License",
   long_description=readme,
   description='A module to calculate the Hilbert transforms of whisker data.',
   author='Marie Tolkiehn',
   author_email='marie_tol@hotmail.com',
   packages=_package_tree('hilbert'),
   install_requires=require,  # external packages as dependencies
   include_package_data=True
)