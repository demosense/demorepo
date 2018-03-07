from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(name='demorepo',
      version='1.0',
      description='Tool to manage a monorepo, where projects can be general projects (code language, build and test management...).',
      author='Javier Cozar',
      author_email='javier.cozar@demosense.com',
      packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_dir={'': 'src'}
      )
