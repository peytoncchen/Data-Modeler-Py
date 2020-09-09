"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['datamodeler.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True,
           'site_packages': True,
           'iconfile': 'py2appfiles/Mouseiconv5.icns',
           'packages': ['statsmodels', 'pandas', 'xlsxwriter'],
           'plist': { 'CFBundleName': 'Data Modeler', 'CFBundleIdentifier': 'com.peyton.datamodeler',
                     'CFBundleVersion': '1.1.0', 'NSHumanReadableCopyright': 'Copyright 2020 Peyton Chen'}
        }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
