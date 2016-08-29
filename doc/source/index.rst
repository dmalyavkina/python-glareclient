Python Bindings for the Glare Artifact Repository
=================================================

This is a client for the Glare Artifact Repository. There's :doc:`a Python API <ref/index>` (the :mod:`glareclient` module) and a :doc:`command-line script<man/glare>` (installed as :program:`glare`).

Python API
----------


Python API Reference
~~~~~~~~~~~~~~~~~~~~


Command-line Tool Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   man/glare

Command-line Tool
-----------------
In order to use the CLI, you must provide your OpenStack username, password, tenant, and auth endpoint. Use the corresponding configuration options (``--os-username``, ``--os-password``, ``--os-tenant-id``, and ``--os-auth-url``) or set them in environment variables::

    export OS_USERNAME=user
    export OS_PASSWORD=pass
    export OS_TENANT_ID=b363706f891f48019483f8bd6503c54b
    export OS_AUTH_URL=http://auth.example.com:5000/v2.0

The command line tool will attempt to reauthenticate using your provided credentials for every request. You can override this behavior by manually supplying an auth token using ``--os-image-url`` and ``--os-auth-token``. You can alternatively set these environment variables::

    export OS_IMAGE_URL=http://glare.example.org:9494/
    export OS_AUTH_TOKEN=3bcc3d3a03f44e3d8377f9247b0ad155

Once you've configured your authentication parameters, you can run ``glare help`` to see a complete listing of available commands.

See also :doc:`/man/glare`.

Release Notes
=============

