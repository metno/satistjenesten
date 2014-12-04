from setuptools import setup

requirements = ['sphinxcontrib-napoleon']
setup(name='satistjenesten',
        packages=['satistjenesten', 'tests'],
        package_dir={'satistjenesten': 'satistjenesten'},
        author='Mikhail Itkin',
        install_requires=requirements,
        description='resampler and netcdf IO')
