# -*- coding: utf-8 -*-
from distutils.core import setup, Extension

model_compressor = [Extension('core', sources=['./core/compress/compressor.cpp'], extra_compile_args=['-std=c++11'])]

setup(name='model_compressor',
      version='1.0',
      description='compressor json like orm models to binary format',
      ext_modules=model_compressor,
      author="zpoint",
      author_email="zp0int@qq.com",
      url="https://github.com/zpoint/model-compressor",
      packages=['model_adaptor']
      )
