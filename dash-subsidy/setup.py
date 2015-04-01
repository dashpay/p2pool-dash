from distutils.core import setup, Extension

dash_module = Extension('dash_subsidy', sources = ['dash_subsidy.cpp'])

setup (name = 'dash_subsidy',
       version = '1.0',
       description = 'Subsidy function for dash',
       ext_modules = [dash_module])
