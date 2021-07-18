Rest Results API
================

.. _api-test_results-project-list:

List test results of a project
------------------------------

List all test results from all submissions of a given project.

.. literalinclude :: generated/projects/projects_id_tests-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/projects/projects_id_tests-GET-attributes.csv
   :delim: |

An example could look as follows:

.. literalinclude :: generated/projects/projects_id_tests-GET-curl.sh
   :language: bash

which might give a result like this:

.. literalinclude :: generated/projects/projects_id_tests-GET-response.json
   :language: json


.. _api-test_results-project-get:

Get single test result of a project
-----------------------------------

Retrieve a specific test result from a project.

.. literalinclude :: generated/projects/projects_id_tests_id-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/projects/projects_id_tests_id-GET-attributes.csv
   :delim: |

An example could look as follows:

.. literalinclude :: generated/projects/projects_id_tests_id-GET-curl.sh
   :language: bash

which might give a result like this:

.. literalinclude :: generated/projects/projects_id_tests_id-GET-response.json
   :language: json

.. _api-test_results-project-modify:

Modify test results of a project
--------------------------------

Modify the fields of an existing test result. All fields have to be given (even the ones that are unchanged).

.. literalinclude :: generated/projects/projects_id_tests_id-PUT-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/projects/projects_id_tests_id-PUT-attributes.csv
   :delim: |

An example could look as follows:

.. literalinclude :: generated/projects/projects_id_tests_id-PUT-curl.sh
   :language: bash

which might give a result like this:

.. literalinclude :: generated/projects/projects_id_tests_id-PUT-response.json
    :language: json

.. _api-test_results-project-delete:

Delete test results of a project
--------------------------------

Deletes a test result from a project. This can not be undone!

.. literalinclude :: generated/projects/projects_id_tests_id-DELETE-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/projects/projects_id_tests_id-DELETE-attributes.csv
   :delim: |

An example could look as follows:

.. literalinclude :: generated/projects/projects_id_tests_id-DELETE-curl.sh
   :language: bash