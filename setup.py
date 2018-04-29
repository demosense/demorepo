from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(name='demorepo',
      version='1.0',
      description='Tool to manage a monorepo, where projects can be general projects '
                  '(code language, build and test management...).',
      author='Javier Cozar',
      author_email='javier.cozar@demosense.com',
      packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_dir={'': 'src'},
      install_requires=[
          'requests>=2.18,<2.19',
          'GitPython>=2.1,<2.2',
          'PyYAML>=3.12,<3.13'
      ],
      entry_points={
          'console_scripts': [
              'demorepo = demorepo.__main__:main'
          ]
      },

      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      )
