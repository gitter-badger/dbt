#!/usr/bin/env python
from setuptools import setup, find_packages
import os.path

package_name = "dbt"
package_version = "0.1.0-SNAPSHOT"

config_dir = os.path.join(os.path.expanduser('~'), '.dbt')

sample_profiles_file = "sample.profiles.yml"
sample_profiles_contents = ""
with open(sample_profiles_file) as fh:
    sample_profiles_contents = fh.read()

data_files = []
if not os.path.exists(config_dir):
    os.path.makedirs(config_dir)

config_file = os.path.join(config_dir, 'profiles.yml')
if not os.path.exists(config_file):

    with open(config_file, 'w') as fh:
        fh.write(sample_profiles_contents)

setup(
  name=package_name,
  version=package_version,
  packages=find_packages(),
  data_files=data_files,
  scripts=[
    'scripts/dbt',
  ],
  install_requires=[
    'argparse>=1.2.1',
    'Jinja2>=2.8',
    'PyYAML>=3.11',
    'psycopg2==2.6.1',
  ],
)
