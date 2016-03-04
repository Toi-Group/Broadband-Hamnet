from setuptools import setup
setup(
    name = 'TOIChat',
    version = "0.4alpha",
    packages = ['src.pi_scripts.modules', \
                'src.pi_scripts.modules.protobuf'],

    # Project users protobuf
    #
    install_requires = ['protobuf==3.0.0b2'],

    # metadata for upload to PyPI
    author = "TOI-Group",
    url = "https://sites.google.com/a/temple.edu/broadband-mcomm/",

    # Classifier reference:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Telecommunications Industry',
          'Natural Language :: English',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Unix Shell',
          'Programming Language :: Python :: 3.5',
          'Topic :: Communications :: Chat',
          ],
)