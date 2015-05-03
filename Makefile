all:
	pyinstaller --distpath=./bin/ -F --clean --name=codegen ./src/compiler.py
