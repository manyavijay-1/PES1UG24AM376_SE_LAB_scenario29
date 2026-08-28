# Lab 1: Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering | PES University – Dept. of CSE
**Problem Statement #29 — Smart Cities, Transport & Logistics**

## Municipal Infrastructure Damage Reporting App

A citizen portal for reporting road potholes, broken streetlights, and water pipeline leaks
using geotagged photos, with automated ticket dispatch to the relevant municipal
engineering department.

**Actors:** Citizen Reporter, Municipal Engineer, GIS Map Service (supporting system actor)

---

## Repository Contents

| File | Description |
|---|---|
| [`Lab1_Report.docx`](./Lab1_Report.docx) | Consolidated report combining all three deliverables below into a single document |
| [`requirements_table.xlsx`](./requirements_table.xlsx) | Requirements table — 5 Functional (FR-001–FR-005) and 2 Non-Functional (NFR-001–NFR-002) requirements |
| [`use_case_diagram.drawio`](./use_case_diagram.drawio) | Editable UML use-case diagram source (draw.io) |
| [`use_case_diagram.pdf`](./use_case_diagram.pdf) | Exported UML use-case diagram |
| [`use_case_flow.docx`](./use_case_flow.docx) | Use-case flow specification (editable) |
| [`use_case_flow.pdf`](./use_case_flow.pdf) | Use-case flow specification (exported) |

## Deliverable Summary

### 1. Requirements Table
5 FRs + 2 NFRs, each with Req ID, Type, Description, Priority, measurable Acceptance
Criteria, and Rationale.

### 2. UML Use-Case Diagram
Models 3 actors (**Citizen Reporter**, **Municipal Engineer**, **GIS Map Service**) and 8 use
cases, including:
- 4 `«include»` relationships (mandatory reused behavior)
- 1 `«extend»` relationship (optional/conditional behavior — *Draft Offline Report* extends
  *Report Infrastructure Damage*)

### 3. Use-Case Flow Specification
One-page flow for **UC-01: Report Infrastructure Damage**, covering Preconditions,
Postconditions, a 7-step Main Success Scenario, and one Alternate Flow (GPS metadata
unavailable → manual pin drop).

---

## How to View

- **Diagram source:** open `use_case_diagram.drawio` at [draw.io](https://app.diagrams.net) or in the VS Code Draw.io extension.
- **Word/Excel files:** open with Microsoft Word / Excel, LibreOffice, or Google Docs/Sheets.
- **PDFs:** open with any PDF viewer.

## Author

*PES University — SE Lab 1 Submission - PES1UG24AM376*
