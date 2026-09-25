# AGENTS.md

## Project overview
This repository contains a small Python dashboard app built with Streamlit and pandas.

- Main entry point: `main.py`
- Runtime: Python 3
- Primary UI library: Streamlit
- Data handling: pandas
- Data file: `vendas.csv` (created automatically if it does not exist)

## Working conventions
- Keep the application behavior aligned with the current Brazilian Portuguese UI text.
- Prefer small, explicit changes in `main.py` rather than large rewrites.
- Preserve the current Streamlit layout and naming conventions unless there is a clear reason to change them.
- When adding new filters, metrics, or tabs, keep the code readable and easy to follow.

## Run and validate
From the repository root:

```bash
python -m streamlit run main.py
```

To validate syntax after changes:

```bash
python -m py_compile main.py
```

## Typical app behavior
- If `vendas.csv` is missing, the app generates sample sales data automatically.
- The sidebar allows filtering by category.
- Summary metrics show total revenue and number of orders.
- There are two tabs: monthly evolution and data table export.

## Agent guidance
- Prefer simple, targeted edits over broad refactors.
- Keep the app self-contained and avoid adding unnecessary dependencies.
- If you introduce a new feature, make sure it still works with the generated CSV dataset and the Streamlit UI.
- For debugging, run the app locally and verify that the dashboard renders and the download/export action still works.
