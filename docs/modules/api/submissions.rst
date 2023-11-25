Submissions API
===============

.. _api-submissions-list:

List submissions of a project
-----------------------------

List all submissions of a given project.

.. literalinclude :: generated/submissions/projects_id_submissions-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/submissions/projects_id_submissions-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/submissions/projects_id_submissions-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/submissions/projects_id_submissions-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/submissions/projects_id_submissions-GET-response.json
   :language: json


.. _api-submissions-new:

Create new submission
---------------------

Create a new, empty submission for the project.

.. literalinclude :: generated/submissions/projects_id_submissions-POST-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/submissions/projects_id_submissions-POST-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/submissions/projects_id_submissions-POST-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/submissions/projects_id_submissions-POST-curl.ps1
         :language: PowerShell

which might give a result like this:

.. literalinclude :: generated/submissions/projects_id_submissions-POST-response.json
    :language: json


.. _api-submissions-get:

Get single submission of a project
----------------------------------

Retrieve a specific submission from a project.

.. literalinclude :: generated/submissions/projects_id_submissions_id-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/submissions/projects_id_submissions_id-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/submissions/projects_id_submissions_id-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/submissions/projects_id_submissions_id-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/submissions/projects_id_submissions_id-GET-response.json
   :language: json

.. _api-submissions-modify:

Modify submissions of a project
-------------------------------

Modify the fields of an existing submission. All fields have to be given (even the ones that are unchanged).

.. literalinclude :: generated/submissions/projects_id_submissions_id-PUT-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/submissions/projects_id_submissions_id-PUT-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/submissions/projects_id_submissions_id-PUT-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/submissions/projects_id_submissions_id-PUT-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/submissions/projects_id_submissions_id-PUT-response.json
    :language: json


.. _api-submissions-delete:

Delete submissions of a project
-------------------------------

Deletes a submission and all its associated data (like test results) from a project. This can not be undone!

.. literalinclude :: generated/submissions/projects_id_submissions_id-DELETE-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/submissions/projects_id_submissions_id-DELETE-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/submissions/projects_id_submissions_id-DELETE-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/submissions/projects_id_submissions_id-DELETE-curl.ps1
         :language: powershell
