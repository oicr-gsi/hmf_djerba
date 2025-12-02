#! /usr/bin/env python3

"""
Setup script for hmf_djerba
"""

from setuptools import setup, find_packages

with open('src/lib/hmf_djerba/version.py') as version_file:
    exec(version_file.read()) # sets __version__
package_root = 'src/lib'

# list of wildcards, intended to capture ancillary files for plugins/helpers/mergers
# TODO make this neater and/or introduce stronger naming conventions
install_wildcards = [
    '*.bed',
    '*.ini',
    '*.json',
    '*.html',
    '*.txt',
    '*.r',
    '*.R',
    'data/*',
    'html/*',
    'resources/*',
    'R/*',
    'r/*',
    'Rscripts/*',
    'templates/*'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hmf_djerba',
    version=__version__,
    scripts=[],
    packages=find_packages(where=package_root),
    package_dir={'' : package_root},
    package_data={
        'djerba.plugins.fusion': install_wildcards,
        'djerba.plugins.genomic_landscape': install_wildcards,
        'djerba.plugins.hmf.wgts.cnv_purple': install_wildcards,
        'djerba.plugins.hmf.wgts.common.cnv': install_wildcards,
        'djerba.plugins.hmf.wgts.snv_indel': install_wildcards,
    },
    install_requires=[
        'djerba',
        'configparse',
        'email_validator',
        'jsonschema',
        'lets-plot',
        'mako',
        'markdown',
        'matplotlib',
        'numpy>2',
        'pandas',
        'pdfkit',
        'plotnine',
        'pycairo',
        'pyinstaller',
        'PyPDF2',
        'requests',
        'seaborn',
        'statsmodels',
    ],
    python_requires='>=3.10.6',
    author="Iain Bancarz",
    author_email="ibancarz [at] oicr [dot] on [dot] ca",
    description="Create reports from metadata and workflow output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oicr-gsi/djerba",
    keywords=['cancer', 'bioinformatics'],
    license='GPL 3.0',
)
