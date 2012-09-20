#!/usr/bin/env python
import subprocess
import shutil
import glob
import os
import re

def compile_coffeescript(inpath):
	outpath = '%s.js' % inpath
	print ' - Coffee:\t%s -> %s' % (inpath, outpath)

	subprocess.check_output('coffee -o compiler-output -c "%s"' % inpath, shell=True)
	shutil.move(glob.glob('./compiler-output/*.js')[0], outpath)
	shutil.rmtree('compiler-output')

def compile_less(inpath):
	outpath = '%s.css' % inpath
	print ' - LESS:\t%s -> %s' % (inpath, outpath)

compilers = {
	r'.+\.coffee$': compile_coffeescript,
	r'.+\.less$': compile_less,
}


def compress_js(inpath):
	outpath = os.path.splitext(inpath)[0] + '.c.js'
	print ' - YUI JS:\t%s -> %s' % (inpath, outpath)
	subprocess.check_output('yui-compressor --nomunge --disable-optimizations -o "%s" "%s"' % (outpath, inpath), shell=True)

def compress_css(inpath):
	outpath = os.path.splitext(inpath)[0] + '.c.css'
	print ' - YUI CSS:\t%s -> %s' % (inpath, outpath)
	subprocess.check_output('yui-compressor -o "%s" "%s"' % (outpath, inpath), shell=True)

compressors = {
	r'.+[^\.][^mc]\.js$': compress_js,
	r'.+[^\.][^mc]\.css$': compress_css,
}


def traverse(fx):
	plugins_path = './ajenti/plugins'
	for plugin in os.listdir(plugins_path):
		path = os.path.join(plugins_path, plugin, 'content')
		if os.path.exists(path):
			for name in os.listdir(path):
				file_path = os.path.join(path, name)
				fx(file_path)
				
def compile(file_path):
	for pattern in compilers:
		if re.match(pattern, file_path):
			compilers[pattern](file_path)

def compress(file_path):
	for pattern in compressors:
		if re.match(pattern, file_path):
			compressors[pattern](file_path)



traverse(compile)
traverse(compress)
