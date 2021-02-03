# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

current_version = str('1.5.5')

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stackuchin',

    version=current_version,

    description='CLI for Stackuchin - Automatically create, update and delete AWS CloudFormation stacks '
                'in multiple AWS accounts and regions at the same time',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/Rungutan/stackuchin',

    download_url='https://github.com/Rungutan/stackuchin/archive/{}.tar.gz'.format(current_version),

    author='Rungutan',

    author_email='support@rungutan.com',

    classifiers=[  # Optional
        # How mature is this project?
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Audience
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',

        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing :: Acceptance',
        'Topic :: Software Development :: Testing :: BDD',
        'Topic :: Software Development :: Testing :: Mocking',
        'Topic :: Software Development :: Testing :: Traffic Generation',
        'Topic :: Software Development :: Testing :: Unit',

        # License
        'License :: OSI Approved :: MIT License',

        # Supported Python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='stackuchin stackuchin-cli stackuchin_cli cli aws cloudformation stacks deployment integration'
             'cotinuous continuos devops tools',

    package_dir={'': 'src'},

    packages=find_packages(where='src'),

    python_requires='>=3.5, <4',

    install_requires=['simplejson', 'boto3', 'botocore', 'pyyaml', 'requests'],

    extras_require={
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'stackuchin=stackuchin:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/Rungutan/stackuchin/issues',
        'Source': 'https://github.com/Rungutan/stackuchin/',
    }
)
