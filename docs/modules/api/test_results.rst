Rest Results API
================

.. _api-test_results-project-list:

List test results of a project
------------------------------

List all test results from all submissions of a given project.

.. literalinclude :: generated/test_results/projects_id_tests-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_tests-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_tests-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_tests-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_tests-GET-response.json
   :language: json


.. _api-test_results-project-get:

Get single test result of a project
-----------------------------------

Retrieve a specific test result from a project.

.. literalinclude :: generated/test_results/projects_id_tests_id-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_tests_id-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_tests_id-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_tests_id-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_tests_id-GET-response.json
   :language: json

.. _api-test_results-project-modify:

Modify test results of a project
--------------------------------

Modify the fields of an existing test result. All fields have to be given (even the ones that are unchanged).

.. literalinclude :: generated/test_results/projects_id_tests_id-PUT-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_tests_id-PUT-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_tests_id-PUT-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_tests_id-PUT-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_tests_id-PUT-response.json
    :language: json

.. _api-test_results-project-delete:

Delete test results of a project
--------------------------------

Deletes a test result from a project. This can not be undone!

.. literalinclude :: generated/test_results/projects_id_tests_id-DELETE-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_tests_id-DELETE-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_tests_id-DELETE-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_tests_id-DELETE-curl.ps1
         :language: powershell


.. _api-test_results-submissions-list:

List test results of a submission
---------------------------------

List all test results from a specific submission of a given project.

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_submissions_id_tests-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests-GET-response.json
   :language: json


.. _api-test_results-submissions-create:

Add new test result to a submission
-----------------------------------

Add a new test result to the submission.

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_submissions_id_tests-POST-attributes.csv
   :delim: |

An example to create an empty test result could look like this:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-empty-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-empty-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-empty-response.json
   :language: json

Or an example to create a test with some initial results:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-nonempty-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-nonempty-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests-POST-nonempty-response.json
   :language: json


.. _api-test_results-submissions-get:

Get single test result of a submission
--------------------------------------

Retrieve a specific test result from a submission.

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_submissions_id_tests_id-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-GET-response.json
   :language: json


.. _api-test_results-submissions-modify:

Modify test results of a submission
-----------------------------------

Modify the fields of an existing test result. All fields have to be given (even the ones that are unchanged).

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-PUT-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_submissions_id_tests_id-PUT-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-PUT-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-PUT-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-PUT-response.json
    :language: json


.. _api-test_results-submissions-delete:

Delete test results of a submission
-----------------------------------

Deletes a test result from a submission. This can not be undone!

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-DELETE-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_submissions_id_tests_id-DELETE-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-DELETE-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id-DELETE-curl.ps1
         :language: powershell


.. _api-test_results-history:

History of a test result measurement
------------------------------------

Retrieves the history of a measurement for a given test.
The history is extracted for all test results of that project that belong to a submission
which has the same *reference relevant properties* as the submission the current test belongs to.

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id_history-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/test_results/projects_id_submissions_id_tests_id_history-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id_history-GET-limited-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id_history-GET-limited-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/test_results/projects_id_submissions_id_tests_id_history-GET-unlimited-response.json
    :language: json
