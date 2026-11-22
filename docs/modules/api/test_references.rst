Rest References API
===================

.. _api-test_references-reference_set-list:

List test references of a reference set
---------------------------------------

List all test references from a reference set.
Each test reference contains a ``measurements`` list. A measurement has a ``name``,
typed ``value`` (which may be null), and an optional ``source`` TestResult id.

.. literalinclude :: generated/test_references/projects_id_references_id_tests-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_references/projects_id_references_id_tests-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_references/projects_id_references_id_tests-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_references/projects_id_references_id_tests-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_references/projects_id_references_id_tests-GET-response.json
   :language: json


.. _api-test_references-reference_set-create:

Add new test reference to a reference set
-----------------------------------------

Add a new test reference to the reference set.
Provide ``measurements`` as a list of named entries. If an entry omits
``source``, the optional ``default_source`` is used.

.. literalinclude :: generated/test_references/projects_id_references_id_tests-POST-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_references/projects_id_references_id_tests-POST-attributes.csv
   :delim: |

An example to create a new test reference could look like this:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_references/projects_id_references_id_tests-POST-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_references/projects_id_references_id_tests-POST-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_references/projects_id_references_id_tests-POST-response.json
   :language: json


.. _api-test_references-reference_set-get:

Get single test reference of a reference set
--------------------------------------------

Retrieve a specific test reference from a reference set.

.. literalinclude :: generated/test_references/projects_id_references_id_tests_id-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_references/projects_id_references_id_tests_id-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_references/projects_id_references_id_tests_id-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_references/projects_id_references_id_tests_id-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_references/projects_id_references_id_tests_id-GET-response.json
   :language: json


.. _api-test_references-reference_set-modify:

Modify test references of a reference set
-----------------------------------------

Modify an existing test reference. PUT replaces its measurements when
``measurements`` is provided. PATCH upserts measurements by name; use
``{"name": "measurement-name", "delete": true}`` to remove one. A null
``value`` is retained as a measurement value and does not remove the entry.

.. literalinclude :: generated/test_references/projects_id_references_id_tests_id-PUT-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_references/projects_id_references_id_tests_id-PUT-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_references/projects_id_references_id_tests_id-PUT-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_references/projects_id_references_id_tests_id-PUT-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_references/projects_id_references_id_tests_id-PUT-response.json
    :language: json


.. _api-test_references-reference_set-delete:

Delete test reference of a reference set
----------------------------------------

Deletes a test reference from a reference set. This can not be undone!

.. literalinclude :: generated/test_references/projects_id_references_id_tests_id-DELETE-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_references/projects_id_references_id_tests_id-DELETE-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_references/projects_id_references_id_tests_id-DELETE-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_references/projects_id_references_id_tests_id-DELETE-curl.ps1
         :language: powershell
