from setuptools import setup, find_packages

setup(
    name='PhoMa',
    version='0.0.1',
    description='Easily browse and download latest photos from your phone',
    url='https://github.com/MarSoft/PhoMa',
    license='MIT',
    author='Semyon Maryasin',
    author_email='simeon@maryasin.name',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ],
    },
    package_data={
        'static': 'PhoMa/static/*',
        'templates': 'PhoMa/templates/*',
    },
    classifiers=[
        'Private :: Do Not Upload',
    ],
)
