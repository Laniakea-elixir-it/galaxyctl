'''
Galaxyctl
'''

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

import sys
def is_virtual():
    """ Return if we run in a virtual environtment. """
    # Check supports venv && virtualenv
    return (getattr(sys, 'base_prefix', sys.prefix) != sys.prefix or
            hasattr(sys, 'real_prefix'))

def get_config_dir():
  path='/etc/galaxyctl'
  if is_virtual() is True:
    path = sys.prefix + '/etc/galaxyctl/'
  return path

import ast, os, re
SOURCE_DIR = "galaxyctl"

with open('%s/__init__.py' % SOURCE_DIR, 'rb') as f:
    init_contents = f.read().decode('utf-8')

    def get_var(var_name):
        pattern = re.compile(r'%s\s+=\s+(.*)' % var_name)
        match = pattern.search(init_contents).group(1)
        return str(ast.literal_eval(match))

    version = get_var("__version__")

setup(
  name='galaxyctl',
  version=version,
  description='galaxy,onedata and luks volume management',
  long_description=readme(),
  url='https://github.com/mtangaro/galaxyctl',
  author='Marco Antonio Tangaro, Federico Zambelli',
  author_email='ma.tangaro@ibiom.cnr.it', 
  license='GPL-3.0',
  packages=['galaxyctl'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
  ],
  keywords='galaxy web server',
  scripts=['bin/galaxyctl'],
  data_files=[
    (get_config_dir(), ['config/galaxyctl.ini'])
  ],
)
