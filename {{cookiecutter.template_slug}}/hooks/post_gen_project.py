import os
from glob import glob

LICENSE_ID = '{{ cookiecutter.license_id }}'

os.rename('LICENSE.{{ cookiecutter.license_id }}', 'LICENSE')

if LICENSE_ID == 'Unlicense':
    os.rename('LICENSE', 'UNLICENSE')

if 'GPL' in LICENSE_ID:
    os.rename('LICENSE', 'COPYING')

for license_file in glob('LICENSE.*'):
    os.unlink(license_file)
