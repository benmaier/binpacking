from setuptools import setup

setup(name='binpacking',
      version='0.1',
      description='Distributes a list of weights to a fixed number of bins while keeping the bins'' volumes approximately equal',
      url='https://www.github.com/benmaier/binpacking',
      author='Benjamin F. Maier',
      author_email='bfmaier@physik.hu-berlin.de',
      license='MIT',
      packages=['binpacking'],
      install_requires=[
          'numpy',
      ],
      zip_safe=False)
