from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

FIXED_GBP_TO_INR = 105.50
BASE_URL = "https://books.toscrape.com/catalogue/"


def get_category_urls() -> list[str]:
    response = requests.get("https://books.toscrape.com", timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    urls: list[str] = []
    seen: set[str] = set()

    for link in soup.select("ul.nav-list li ul li a"):
        href = link.get("href")
        if not href or "/category/books/" not in href:
            continue
        full_url = "https://books.toscrape.com/" + href.lstrip("/")
        canonical = full_url.split("?")[0]
        if canonical not in seen:
            seen.add(canonical)
            urls.append(canonical)

    return urls[:8]


def fetch_book_rows(category_name: str, category_url: str) -> list[dict]:
    rows: list[dict] = []
    page_number = 1
    while page_number <= 2:
        page_url = category_url
        if page_number > 1:
            if page_url.endswith("/index.html"):
                page_url = page_url.replace("/index.html", f"/page-{page_number}.html")
            elif page_url.endswith("/"):
                page_url = f"{page_url}page-{page_number}.html"
            else:
                page_url = f"{page_url}/page-{page_number}.html"

        response = requests.get(page_url, timeout=20)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")
        if not products:
            break

        for article in products:
            title_tag = article.select_one("h3 a")
            title = title_tag.get("title") if title_tag else ""
            title = (title or (title_tag.text.strip() if title_tag else "")).strip()

            price_tag = article.select_one("p.price_color")
            price_text = price_tag.get_text(strip=True) if price_tag else ""

            rating_tag = article.select_one("p.star-rating")
            rating_text = "" if not rating_tag else rating_tag.get("class", [""])[-1]

            availability_tag = article.select_one("p.availability")
            availability_text = availability_tag.get_text(" ", strip=True) if availability_tag else ""

            rows.append(
                {
                    "title": title,
                    "price_gbp_raw": price_text,
                    "rating_raw": rating_text,
                    "availability_raw": availability_text,
                    "category": category_name,
                }
            )

        page_number += 1

    return rows


def parse_price(value: str) -> float:
    cleaned = value.replace("£", "").replace(",", "").strip()
    if not cleaned:
        return float("nan")
    try:
        return float(cleaned)
    except ValueError:
        return float("nan")


def parse_rating(value: str) -> int:
    mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }
    key = (value or "").strip()
    if key in mapping:
        return mapping[key]
    return int(float("nan"))


def parse_availability(value: str) -> int:
    text = (value or "").lower()
    return 1 if "in stock" in text else 0


def build_dataset() -> pd.DataFrame:
    rows: list[dict] = []
    for category_url in get_category_urls():
        category_name = category_url.split("/category/books/")[-1].split("/")[0].replace("_", " ").title()
        rows.extend(fetch_book_rows(category_name, category_url))

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["title"]).copy()
    df["price_gbp"] = df["price_gbp_raw"].apply(parse_price)
    df["rating"] = df["rating_raw"].apply(parse_rating)
    df["in_stock"] = df["availability_raw"].apply(parse_availability)
    df["category"] = df["category"].fillna("Unknown")

    for numeric_col in ["price_gbp", "rating"]:
        median_value = df[numeric_col].median()
        df[numeric_col] = df[numeric_col].fillna(median_value)

    df["price_inr"] = df["price_gbp"] * FIXED_GBP_TO_INR
    df["price_gbp"] = df["price_gbp"].astype(float)
    df["rating"] = df["rating"].astype(int)
    df["in_stock"] = df["in_stock"].astype(int)

    return df


def build_sqlite_db(df: pd.DataFrame, db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("CREATE TABLE categories (category_id INTEGER PRIMARY KEY, category_name TEXT UNIQUE)")
    cur.execute("CREATE TABLE books (book_id INTEGER PRIMARY KEY, title TEXT, price_gbp REAL, price_inr REAL, rating INTEGER, in_stock INTEGER, category_id INTEGER REFERENCES categories(category_id))")

    category_lookup = {}
    for category_name in sorted(df["category"].unique()):
        category_id = len(category_lookup) + 1
        category_lookup[category_name] = category_id
        cur.execute(
            "INSERT INTO categories (category_id, category_name) VALUES (?, ?)",
            (category_id, category_name),
        )

    for _, row in df.iterrows():
        book_values = (
            row["title"],
            float(row["price_gbp"]),
            float(row["price_inr"]),
            int(row["rating"]),
            int(row["in_stock"]),
            category_lookup[row["category"]],
        )
        cur.execute(
            "INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id) VALUES (?, ?, ?, ?, ?, ?)",
            book_values,
        )

    conn.commit()
    conn.close()


def run_queries(connection: sqlite3.Connection) -> list[tuple[str, str, pd.DataFrame]]:
    queries = [
        (
            "SELECT * FROM books WHERE in_stock = 1 AND price_gbp < 40 ORDER BY price_gbp DESC;",
            "Select in-stock books under 40 GBP",
        ),
        (
            "SELECT b.title, b.price_inr, c.category_name FROM books b JOIN categories c ON b.category_id = c.category_id ORDER BY b.price_inr DESC LIMIT 10;",
            "Top 10 most expensive books by price_inr",
        ),
        (
            "SELECT title, price_gbp FROM books ORDER BY price_gbp ASC LIMIT 5;",
            "Five cheapest books",
        ),
        (
            "SELECT DISTINCT c.category_name FROM categories c ORDER BY c.category_name;",
            "Distinct category names",
        ),
        (
            "SELECT b.title, c.category_name FROM books b JOIN categories c ON b.category_id = c.category_id WHERE c.category_id IN (1, 2, 3) ORDER BY b.title;",
            "Books in categories 1, 2, or 3",
        ),
        (
            "SELECT b.title, c.category_name, b.rating, b.price_inr FROM books b JOIN categories c ON b.category_id = c.category_id WHERE b.rating >= 4 ORDER BY c.category_name, b.rating DESC, b.price_inr DESC;",
            "Join example: books rated 4+",
        ),
    ]

    results: list[tuple[str, str, pd.DataFrame]] = []
    for query, label in queries:
        frame = pd.read_sql_query(query, connection)
        results.append((label, query, frame))
    return results


def save_queries_markdown(results: list[tuple[str, str, pd.DataFrame]], output_path: Path) -> None:
    sections: list[str] = []
    for idx, (label, query, df) in enumerate(results, start=1):
        sections.append(f"## Query {idx}: {label}\n\n```sql\n{query}\n```\n\n{df.to_string(index=False)}\n")
    output_path.write_text("\n\n".join(sections), encoding="utf-8")


def verify_join_equivalence(connection: sqlite3.Connection, category_df: pd.DataFrame, books_df: pd.DataFrame) -> pd.DataFrame:
    sql_join = """
        SELECT b.title, c.category_name, b.rating, b.price_inr
        FROM books b
        JOIN categories c ON b.category_id = c.category_id
        WHERE b.rating >= 4
        ORDER BY c.category_name, b.rating DESC, b.price_inr DESC
    """
    sql_result = pd.read_sql_query(sql_join, connection)
    pd_result = books_df.merge(category_df, left_on="category_id", right_on="category_id", how="inner")
    pd_result = pd_result[pd_result["rating"] >= 4].sort_values(["category_name", "rating", "price_inr"], ascending=[True, False, False])
    pd_result = pd_result[["title", "category_name", "rating", "price_inr"]].reset_index(drop=True)
    comparison = sql_result.reset_index(drop=True).equals(pd_result.reset_index(drop=True))
    print(f"Join equivalence check: {comparison}")
    return sql_result


def main() -> None:
    df = build_dataset()

    if len(df) < 60:
        raise ValueError(f"Scraped dataset is too small: {len(df)} rows found. Need at least 60 books across 3 categories.")

    db_path = Path(__file__).resolve().parent / "zepto_books.db"
    build_sqlite_db(df, db_path)

    conn = sqlite3.connect(db_path)
    categories_df = pd.read_sql_query("SELECT * FROM categories", conn)
    books_df = pd.read_sql_query("SELECT * FROM books", conn)

    results = run_queries(conn)
    output_path = Path(__file__).resolve().parent / "queries_output.md"
    save_queries_markdown(results, output_path)

    sql_join = pd.read_sql_query(
        "SELECT b.title, c.category_name, b.rating, b.price_inr FROM books b JOIN categories c ON b.category_id = c.category_id WHERE b.rating >= 4 ORDER BY c.category_name, b.rating DESC, b.price_inr DESC;",
        conn,
    )
    merged = books_df.merge(categories_df, on="category_id", how="inner")
    merged = merged[merged["rating"] >= 4].sort_values(["category_name", "rating", "price_inr"], ascending=[True, False, False])
    merged = merged[["title", "category_name", "rating", "price_inr"]].reset_index(drop=True)

    print("SQL result:\n", sql_join.head(10).to_string(index=False))
    print("\nPandas merge result:\n", merged.head(10).to_string(index=False))
    print("\nEquivalent output:", sql_join.reset_index(drop=True).equals(merged.reset_index(drop=True)))

    conn.close()

    print(f"\nDatabase created at: {db_path}")
    print(f"Total scraped books: {len(df)}")
    print(f"Categories: {sorted(df['category'].unique().tolist())}")


if __name__ == "__main__":
    main()
