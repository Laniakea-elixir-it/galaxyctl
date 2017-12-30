'''
Galaxyctl
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='galaxyctl',
  version='0.1.0a1',
  description='galaxy,onedata and luks volume management',
  long_description=long_description,
  url='https://github.com/mtangaro/galaxyctl',
  author='Marco Antonio Tangaro, Federico Zambelli',
  author_email='ma.tangaro@ibiom.cnr.it', 
  license='MIT',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
  ],
  keywords='galaxy web server',
)
