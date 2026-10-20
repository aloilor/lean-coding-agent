# Feature Specification — Export Invoice as PDF

## Feature

- **ID:** FEAT-004
- **Name:** Export Invoice as PDF
- **Version:** 1.0
- **Status:** Draft

## Objective

Allow authorized users to generate a PDF representation of an invoice so that it can be downloaded, printed, or shared with a customer.

## User Stories

**US-1**
As an accounting user, I want to export an invoice as a PDF so that I can send it to a customer.

**US-2**
As an administrator, I want exported invoices to contain the same financial information shown in the application so that the document can be used as an official invoice copy.

## Scope

The feature includes:

- exporting an existing invoice from the invoice detail page;
- generating a PDF using the current invoice data;
- including company, customer, invoice, tax, line-item, and total information;
- downloading the generated PDF to the user's device.

## Out of Scope

The following are not included in this feature:

- sending the PDF by email;
- automatic PDF generation when an invoice is created;
- storing historical versions of generated PDFs;
- custom invoice templates;
- allowing users to edit the PDF before downloading it.

## Actors and Permissions

The feature is available to:

- Administrators;
- Billing Managers.

Users without permission to view an invoice shall not be able to export it.

## Preconditions

- The user must be authenticated.
- The invoice must already exist.
- The user must have permission to view the invoice.

## Functional Requirements

**FR-1 — Export action**
The invoice detail page shall provide an Export PDF action to authorized users.

**FR-2 — PDF generation**
When the user selects Export PDF, the system shall generate a PDF representing the current invoice.

**FR-3 — Invoice information**
The generated PDF shall include:

- company logo, when configured;
- invoice number;
- issue date;
- due date, when applicable;
- invoice status;
- company name and billing information;
- customer name and billing information;
- invoice line items;
- quantity and unit price for each line item;
- subtotal;
- applicable taxes;
- discounts, when applicable;
- total amount;
- invoice currency.

**FR-4 — File name**
The downloaded file shall follow the naming convention `invoice-{invoiceNumber}.pdf`.

Example: `invoice-INV-2026-00124.pdf`

**FR-5 — Current data**
The generated PDF shall reflect the invoice data available at the moment the export is requested.

**FR-6 — Cancelled invoices**
Cancelled invoices shall remain exportable. Every page of a cancelled invoice's PDF shall display a visible CANCELLED label.

**FR-7 — Download behavior**
After successful generation, the PDF shall be made available to the user as a downloadable file.

## Business Rules

**BR-1 — Invoice currency**
All monetary values shall use the currency assigned to the invoice.

**BR-2 — Consistent tax calculations**
Tax calculations displayed in the PDF shall match the tax calculations displayed in the application.

**BR-3 — Omit inapplicable values**
If a value is not applicable, it may be omitted from the PDF rather than displayed as an empty field.

**BR-4 — Authorization required**
Users shall not be able to export invoices they are not authorized to view.

## Error Handling and Edge Cases

**EC-1 — PDF generation failure**
If PDF generation fails, the user shall remain on the invoice page and an error message shall be displayed.

**EC-2 — Empty optional fields**
Missing optional information, such as a due date or customer secondary address, shall not prevent PDF generation.

**EC-3 — Large invoices**
Invoices containing up to 1,000 line items shall be exportable.

**EC-4 — Special characters**
Customer names, addresses, and invoice descriptions containing supported Unicode characters shall be rendered correctly in the PDF.

**EC-5 — Long descriptions**
Line-item descriptions shall wrap onto additional lines and shall not be truncated.

## Acceptance Criteria

**AC-1 — Successful export**

- **Given** an authorized user is viewing an invoice
- **When** the user selects Export PDF
- **Then** the system generates a PDF
- **And** the generated PDF contains the invoice information defined in FR-3
- **And** the file is made available for download

**AC-2 — File naming**

- **Given** an invoice with invoice number INV-2026-00124
- **When** the invoice is exported
- **Then** the downloaded file is named `invoice-INV-2026-00124.pdf`

**AC-3 — Unauthorized user**

- **Given** a user who is not authorized to export invoices
- **When** the user views an invoice
- **Then** the Export PDF action is not available

**AC-4 — Cancelled invoice**

- **Given** an authorized user is viewing a cancelled invoice
- **When** the user selects Export PDF
- **Then** the system generates the PDF successfully
- **And** every page displays a visible CANCELLED label

**AC-5 — Generation failure**

- **Given** an authorized user requests an invoice export
- **When** the PDF generation process fails
- **Then** no corrupted or incomplete PDF is downloaded
- **And** the user is informed that the export failed

## UI / UX Reference

- The invoice detail page shall contain an Export PDF action.
- The exact placement of the action shall follow the approved invoice detail page design.
- Any mockups attached to this specification are considered illustrative unless explicitly marked as binding.

## Non-Functional Requirements

**NFR-1 — Performance**
PDF generation should normally complete within 3 seconds for invoices containing up to 100 line items.

**NFR-2 — Compatibility**
The generated PDF shall be readable by commonly used PDF readers.

**NFR-3 — Security**
PDF generation shall enforce the same invoice access permissions used by the application.

**NFR-4 — Backward compatibility**
Introducing this feature shall not change the behavior of existing invoice APIs unless explicitly specified elsewhere.

## Dependencies and Assumptions

- Invoice data is already available through the existing invoice domain or API.
- Company billing information is already configured in the system.
- The application already provides invoice access-control rules.
- A standard invoice PDF layout will be used.

## Open Questions

**OQ-1 — Should the company logo appear in the PDF?**
Recommended: yes, using the logo already configured in company settings, because customers expect a branded invoice and no new upload is needed. Affects: FR-3.

**OQ-2 — Should cancelled invoices display a visible CANCELLED label?**
Recommended: yes, on every page, so that a cancelled invoice cannot be mistaken for one that is still payable. Affects: FR-6, AC-4.

**OQ-3 — Should long invoice descriptions wrap freely or be truncated?**
Recommended: wrap in full, because truncation can hide billing details the customer needs. Affects: EC-5.

**OQ-4 — Is a specific PDF layout legally or commercially required?**
Recommended: no specific layout beyond the fields listed in FR-3; the client confirms with their accountant that those fields meet local invoicing rules. Affects: FR-3, Dependencies and Assumptions.

Resolve all open questions before the feature is considered ready for implementation.
