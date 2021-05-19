from setuptools import setup

setup(name='binpacking',
      version='1.4.5',
      description='Heuristic distribution of weighted items to bins (either a fixed number of bins or a fixed number of volume per bin). Data may be in form of list, dictionary, list of tuples or csv-file.',
      url='https://www.github.com/benmaier/binpacking',
      author='Benjamin F. Maier',
      author_email='bfmaier@physik.hu-berlin.de',
      license='MIT',
      packages=['binpacking'],
      setup_requires=['pytest-runner'],
      install_requires=[
          'numpy', 'future',
      ],
      tests_require=['pytest', 'pytest-cov'],
      dependency_links=[
          ],
      entry_points = {
            'console_scripts': [
                    'binpacking = binpacking.binpacking_binary:main',
                ],
            },
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   ],
      zip_safe=False)
