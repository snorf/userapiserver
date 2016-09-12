from setuptools import setup

setup(name='UserApiServer',
      version='1.0',
      description='UserApiServer',
      author='Johan Karlsteen',
      author_email='johan.karlsteen@gmail.com',
      url='https://github.com/snorf/userapiserver',
      install_requires=['Flask>=0.11.1',
                        'Flask_JWT>=0.3.2',
                        'Flask_RESTful>=0.3.5',
                        'Flask_SQLAlchemy>=2.1',
                        'python_bcrypt>=0.3.1',
                        'python_dateutil>=2.5.3'],
     )