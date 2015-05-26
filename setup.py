
from setuptools import find_packages, setup

# based off django's own setup.py

version = __import__('rx-registration').__version__

setup(
    name='django-rx-registration',
    version=version,
    url='http://github.com/shezi/rx-registration/',
    author='Johannes Spielmann, Jochen Wersdörfer',
    author_email='j@spielmannsolutions.com',
    description=('A high-level Python Web framework that encourages '
                 'rapid development and clean, pragmatic design.'),
    license='MIT',
    packages=find_packages(), #exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)