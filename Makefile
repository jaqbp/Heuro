# Build Cython to .pyd file
build:
	python setup.py build_ext --inplace

clean:
	find . -type f -name "*.txt" -exec rm -rf {} \;
