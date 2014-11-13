from setuptools import setup
# from distutils.core import setup

setup(name='satistjenesten',
        packages=['satistjenesten', 'satistjenesten/tests'],
        package_dir={'satistjenesten': 'satistjenesten'},
        author='Mikhail Itkin',
        description='resampler and netcdf IO')
