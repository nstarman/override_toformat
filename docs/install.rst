.. include:: references.txt

.. override_toformat-install:

************
Installation
************

With ``pip`` (recommended)
==========================

To install the latest stable version using ``pip``, use

.. code-block:: bash

    python -m pip install override_toformat

This is the recommended way to install ``override_toformat``.

To install the development version

.. code-block:: bash

    python -m pip install git+https://github.com/nstarman/override_toformat


With ``conda``
==============

Conda is not yet supported.


From Source: Cloning, Building, Installing
==========================================

The latest development version of override_toformat can be cloned from `GitHub
<https://github.com/>`_ using ``git``

.. code-block:: bash

    git clone git://github.com/nstarman/override_toformat.git

To build and install the project (from the root of the source tree, e.g., inside
the cloned ``override_toformat`` directory)

.. code-block:: bash

    python -m pip install [-e] .


Python Dependencies
===================

This packages has the following dependencies:

* `Python`_ >= 3.8

Explicit version requirements are specified in the project `pyproject.toml
<https://github.com/nstarman/override_toformat/blob/main/pyproject.toml>`_. ``pip``
and ``conda`` should install and enforce these versions automatically.
