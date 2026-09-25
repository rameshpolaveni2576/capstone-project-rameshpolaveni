# Data Pipeline

## Goal

This module follows the project brief for a raw-to-relational catalog workflow: scrape books from a public site, clean the fields, apply the required fixed-rate conversion, normalize the data into SQLite tables, and query it with both SQL and pandas.

## Required fixed-rate conversion

`1 GBP = 105.50 INR`

This is the required project-defined baseline for this assignment. It is intentionally fixed and does not require a live API lookup or date reference.

## Cleaning choices

- Currency strings are parsed into floats and stored as `price_gbp`.
- Star ratings are converted from text such as `One`/`Three`/`Five` to integers 1–5.
- Availability text is converted to a boolean-like `in_stock` integer flag.
- Missing numeric values are handled with median imputation to keep the pipeline resilient to messy rows instead of crashing.

## Run

```bash
python data_pipeline/build_database.py
```

This script builds the SQLite database at `data_pipeline/zepto_books.db` and writes the executed query documentation to `data_pipeline/queries_output.md`.

## Schema

```sql
categories(category_id INTEGER PRIMARY KEY, category_name TEXT UNIQUE)
books(book_id INTEGER PRIMARY KEY, title TEXT, price_gbp REAL, price_inr REAL, rating INTEGER, in_stock INTEGER, category_id INTEGER REFERENCES categories(category_id))
```

## Query coverage

The script runs multiple SQL queries covering `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`, and at least one `JOIN`, and it demonstrates the equivalence between `pd.read_sql` and `pandas.merge` for the join result.

## Notes

The workflow is a single end-to-end data-engineering story: scrape → clean → convert → load → query.
