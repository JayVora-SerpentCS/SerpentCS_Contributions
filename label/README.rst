=====================
Mass Label Reporting
=====================

Create and print custom labels for products and other Odoo records. Configure
which record fields appear on each label, choose a label brand and format, and
print the requested number of copies from the record's action menu.

Features
========

* Configure label brands and label formats, including dimensions, margins, and
  cell spacing.
* Build label templates for an Odoo model and select the fields to print.
* Display regular field values, product images, and barcodes.
* Set field order, font size, label visibility, line breaks, and placement.
* Add a label printing action to a model's record form.
* Print multiple copies using a selected brand and label format.

Requirements
============

* Odoo 20.0
* The Odoo ``base`` and ``web`` modules

Installation
============

#. Add the ``label`` module directory to an Odoo addons path.
#. Restart the Odoo server and refresh the Apps list.
#. Find **Mass Label Reporting** in Apps and install it.

Configuration
=============

Label brands and formats
------------------------

Open **Settings → Configuration → Label Configuration**. Select a brand and
review its available formats, or create a brand and format. A format defines
the label height and width in millimetres, page margins, and spacing between
labels.

Label template
--------------

Open **Settings → Configuration → Label Print** and create a template:

#. Enter a template name and select the Odoo model whose records will be
   printed.
#. Add template fields and select each model field, or enable **Python
   Expression** and provide an expression beginning with ``obj.``.
#. Set each field's sequence, display type (Normal, Image, or Barcode), font
   size, and other display options. Image and barcode fields can also have a
   position configured.
#. On the **Advance** tab, add a sidebar action if users should launch this
   template directly from records of the selected model.

Printing labels
===============

#. Open a record of the configured model.
#. Use the **Action** menu and choose the label template.
#. In the print wizard, select the **Brand Name** and **Label Size**, then set
   **Number of Copy**.
#. Click **Print** to generate the label report.

When an image or barcode field's position is left unset, images default to the
right and barcodes to the left. Explicitly configured positions are respected.
Binary image fields and fields identified as barcodes can be rendered even if
their display type is left as **Normal**.

Support
=======

For support, contact Serpent Consulting Services Pvt. Ltd. at
``support@serpentcs.com``.

Credits
=======

Contributors
------------

* Serpent Consulting Services Pvt. Ltd. <support@serpentcs.com>

License
=======

This module is licensed under LGPL-3. See the ``LICENSE`` directory for the
full license text.
