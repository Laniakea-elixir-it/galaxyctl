'''
Galaxyctl
'''

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

def get_config_dir():
  import os, sys
  path='/etc/galaxyctl'
  if not os.geteuid() == 0:
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
  license='MIT',
  packages=['galaxyctl'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
  ],
  keywords='galaxy web server',
  scripts=['bin/galaxyctl', 'bin/luksctl', 'bin/onedatactl'],
  data_files=[(get_config_dir(), ['config/galaxyctl.ini']),
              (get_config_dir(), ['config/luks-cryptdev.ini.sample']),
              (get_config_dir(), ['config/onedatactl.ini.sample'])],
)

print 'prova'
