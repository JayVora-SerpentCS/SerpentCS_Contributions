.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Web Widget Multi Image
==================================

Description
-----------

This module provides the functionality to store multiple images for one record.
All images store in server directory. so database size does not increase.
Usage
------------

To use this module, you need to:

- Add a text field to your model.
- Add " widget = 'image_multi' " attribute inside your text field definition (XML).

Your XML form view definition will look a like:

    ...
    <field name="YOUR_TEXT_FIELD" widget="image_multi"/>
    ...

It will display text field as a signature.

For further information, please visit:

https://www.odoo.com/forum/help-1


Bug Tracker
===========

Credits
=======

Contributors
------------

* Jay Vora <jay.vora@serpentcs.com>
* Meet Dholakia <m.dholakia.serpentcs@gmail.com>

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
