from setuptools import setup

setup(
    name='TabExImg',
    version='1.0.0',
    packages=['luminoth.luminoth', 'luminoth.luminoth.tools', 'luminoth.luminoth.tools.cloud',
              'luminoth.luminoth.tools.server', 'luminoth.luminoth.tools.dataset',
              'luminoth.luminoth.tools.dataset.readers', 'luminoth.luminoth.tools.dataset.readers.object_detection',
              'luminoth.luminoth.tools.dataset.writers', 'luminoth.luminoth.tools.checkpoint',
              'luminoth.luminoth.utils', 'luminoth.luminoth.utils.test', 'luminoth.luminoth.utils.hooks',
              'luminoth.luminoth.models', 'luminoth.luminoth.models.ssd', 'luminoth.luminoth.models.base',
              'luminoth.luminoth.models.fasterrcnn', 'luminoth.luminoth.datasets'],
    url='https://github.com/klemens08/TabExImg',
    license='',
    author='Klemen Sudi',
    author_email='sudiklemens@hotmail.com',
    description='', install_requires=['luminoth', 'xlwt', 'pdf2image']
)
