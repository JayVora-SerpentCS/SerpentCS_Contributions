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

