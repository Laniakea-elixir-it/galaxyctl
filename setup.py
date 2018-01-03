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

setup(
  name='galaxyctl',
  version='0.1.0a1',
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
  scripts=['bin/galaxyctl'],
  data_files=[(get_config_dir(), ['config/galaxyctl.ini'])],
)

print 'prova'
