====================
Partner Credit Limit
====================

Odoo 20.0 addon that blocks sales order confirmation and customer invoice
posting when the commercial customer's credit limit would be exceeded.

Configuration
=============

* Enable Credit Limits in Accounting settings for the relevant company.
* Set the customer's Credit Limit on the Accounting tab.
* Enable Allow Over Credit? on the commercial customer to permit an override.
  This existing override is shared across companies; credit limits and the
  company setting are evaluated for the document's company.

Behavior
========

* Uses Odoo's native calculation: posted receivables plus confirmed sales orders
  still to invoice plus the current document.
* Converts sales order amounts to company currency using the order currency rate.
  Invoices use Odoo 20's company-currency tax totals, including invoice rates.
* Excludes the related sales amount when posting an invoice created from a sales
  order, so the same amount is not counted twice.
* A zero credit limit means unlimited credit, following standard Odoo behavior.
* Vendor bills and customer credit notes are not blocked.
* Salespeople can confirm quotations without accounting-field read permissions;
  only the credit calculation reads those fields with elevated access.

Migration and verification
==========================

See MIGRATION_20.md for the reviewed PDF changes, source compatibility checks,
validation results and installation commands. This addon port does not migrate
an Odoo 19 database to Odoo 20.

Credits
=======

* Serpent Consulting Services Pvt. Ltd. <support@serpentcs.com>
