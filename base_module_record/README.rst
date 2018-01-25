.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==================
Base Module Record
==================

* This module allows you to create a new module without any development.

* It records all operations on objects during the recording session and produce a .ZIP module. So you can create your own module directly from the OpenERP client.

* This version works for creating and updating existing records. It recomputes dependencies and links for all types of widgets (many2one, many2many, ...).

* It also support workflows and demo/update data.

* This should help you to easily create reusable and publishable modules for custom configurations and demo/testing data.
  

Usage
=====
How to use it:

* Run Administration/Customization/Module Creation/Export Customizations As a Module wizard.
* Select datetime criteria in Record From Date field of recording and objects to be recorded and Record module.


Bug Tracker
===========

Credits
=======

Contributors
------------

* Jay Vora <jay.vora@serpentcs.com>
* Meet Dholakia <m.dholakia.serpentcs@gmail.com>.
* Sudhir Arya <sudhir.arya@serpentcs.com>.

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
