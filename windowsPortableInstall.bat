:: Run this on a windows computer with python installed, and it should populate the app folder with the dependencies.
:: Also with git installed
:: The virtual environment it creates also has python. :)

git submodule update --init --recursive

:: Pushd works with powershell, but most computers disable powershell :( Like why tho
:: pushd ./app
cd ./app

call ./setupEnv.bat
call ./venv/Scripts/activate.bat

call ./resetDatabase.bat

call ./venv/Scripts/deactivate.bat

call ./start.bat

::popd
cd ..