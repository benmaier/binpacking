from setuptools import setup

setup(name='binpacking',
      version='1.01',
      description='Aims at optimal distribution of weighted items to bins (either a fixed number of bins or a fixed number of volume per bin). Data may be in form of list, dictionary, list of tuples or csv-file.',
      url='https://www.github.com/benmaier/binpacking',
      author='Benjamin F. Maier',
      author_email='bfmaier@physik.hu-berlin.de',
      license='MIT',
      packages=['binpacking'],
      install_requires=[
          'numpy',
      ],
      dependency_links=[
          ],
      entry_points = {
            'console_scripts': [
                    'binpacking = binpacking.binpacking_binary:main',
                ],
            },
      zip_safe=False)
