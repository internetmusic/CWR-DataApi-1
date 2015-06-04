#!/bin/bash
# This script runs the tests using Jython

if [ "$JYTHON" == "true" ]; then

   git clone https://github.com/yyuu/pyenv.git ~/.pyenv
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"

   echo "Installing Jython"
   pyenv install jython-2.7.0
   pyenv global jython-2.7.0

   eval "$(pyenv init -)"

   echo "Interpreter version:"
   python --version

   echo "Running tests"
   pip install tox

   pip --upgrade virtualenv

   tox -e jython

fi
