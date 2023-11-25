References API
==============

.. _api-references-list:

List reference sets of a project
--------------------------------

List all reference sets of a given project.

.. literalinclude :: generated/references/projects_id_references-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/references/projects_id_references-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/references/projects_id_references-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/references/projects_id_references-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/references/projects_id_references-GET-response.json
   :language: json


.. _api-references-new:

Create new reference set
------------------------

Create a new, empty reference set for the project.

.. literalinclude :: generated/references/projects_id_references-POST-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/references/projects_id_references-POST-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/references/projects_id_references-POST-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/references/projects_id_references-POST-curl.ps1
         :language: PowerShell

which might give a result like this:

.. literalinclude :: generated/references/projects_id_references-POST-response.json
    :language: json


.. _api-references-get:

Get single reference set of a project
-------------------------------------

Retrieve a specific reference set from a project.

.. literalinclude :: generated/references/projects_id_references_id-GET-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/references/projects_id_references_id-GET-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/references/projects_id_references_id-GET-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/references/projects_id_references_id-GET-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/references/projects_id_references_id-GET-response.json
   :language: json

.. _api-references-modify:

Modify reference sets of a project
----------------------------------

Modify the fields of an existing reference set. All fields have to be given (even the ones that are unchanged).

.. literalinclude :: generated/references/projects_id_references_id-PUT-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/references/projects_id_references_id-PUT-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/references/projects_id_references_id-PUT-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/references/projects_id_references_id-PUT-curl.ps1
         :language: powershell

which might give a result like this:

.. literalinclude :: generated/references/projects_id_references_id-PUT-response.json
    :language: json


.. _api-references-delete:

Delete reference sets of a project
----------------------------------

Deletes a reference set and all its associated data (like test result references) from a project. This can not be undone!

.. literalinclude :: generated/references/projects_id_references_id-DELETE-desc.txt

.. csv-table::
   :header-rows: 1
   :file: generated/references/projects_id_references_id-DELETE-attributes.csv
   :delim: |

An example could look as follows:

.. tabs::

   .. group-tab:: Bash

      .. literalinclude :: generated/references/projects_id_references_id-DELETE-curl.sh
         :language: bash

   .. group-tab:: PowerShell

      .. literalinclude :: generated/references/projects_id_references_id-DELETE-curl.ps1
         :language: powershell
