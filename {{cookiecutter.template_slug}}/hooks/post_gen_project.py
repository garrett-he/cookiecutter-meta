import os
from glob import glob

license_id = '{{ cookiecutter.license_id }}'

os.rename('LICENSE.{{ cookiecutter.license_id }}', 'LICENSE')

if license_id == 'Unlicense':
    os.rename('LICENSE', 'UNLICENSE')

if 'GPL' in license_id:
    os.rename('LICENSE', 'COPYING')

for license_file in glob('LICENSE.*'):
    os.unlink(license_file)
