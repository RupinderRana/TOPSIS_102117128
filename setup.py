
from distutils.core import setup
setup(
  name = 'Topsis-102117128',         # How you named your package folder (MyLib)
  packages = ['Topsis-Rupinder'],   # Chose the same as "name"
  version = '1.0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Contains the Topsis package by Rupinder on topsis',   # Give a short description about your library
  author = 'Rupinder Singh Rana ',                   # Type in your name
  author_email = 'rupinderrana0798@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Rupinder_98/Topsis-Rupinder',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RupinderRana/TOPSIS_102117128/archive/refs/tags/1.0.4.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
)
