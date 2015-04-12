from distutils.core import setup, Extension

dash_subsidy_module = Extension('dash_subsidy', sources = ['dash_subsidy.cpp'])

setup (name = 'dash_subsidy',
       version = '1.3',
       description = 'Subsidy function for Dash',
       ext_modules = [dash_subsidy_module])
