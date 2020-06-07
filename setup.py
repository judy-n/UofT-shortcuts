from setuptools import setup

APP = ['UofT.py']
DATA_FILES = [('', ['icons'])]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'uoft.icns',
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    name='UofT',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)
