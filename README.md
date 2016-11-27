# test-binder

A code sprint with a friend from earth sciences to test technologies
like Jupyter, ipywidgets, binder & friends to make computational code
trivially accessible to end-user through a form-based web-interface.

[![Binder](http://mybinder.org/badge.svg)](http://mybinder.org:/repo/nthiery/test-binder/)

## Authors

Tamir Kamai and Nicolas M. Thiéry

## References

- https://mybinder.org
- https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html#
- https://ipython.readthedocs.io/en/stable/interactive/plotting.html
- https://blog.dominodatalab.com/interactive-dashboards-in-jupyter/

## TODO

- [ ] Widgets to upload / download data
- [ ] Automatic execution of the notebook
- [ ] Hiding of the code
- [ ] Make this repo into a pip package for ease of local install
- [ ] Mini workflow manager: input type / processing / output
- [ ] Types for the input

## Local installation

Notes on local installation (Ubuntu/Mint):

    sudo apt install python3
    sudo pip3 install --upgrade pip
    sudo pip3 install jupyter
    sudo pip3 install matplotlib
    sudo pip3 install scipy
    sudo pip3 install pandas
    jupyter nbextension enable --py widgetsnbextension

    python3 -m ipykernel install --user
