import duckdb as db
from dataclasses import dataclass


@dataclass
class TableAttributes:
    col_names: list[str]
    col_types: list[str]
    tbl_schema: str


def get_tbl_attr(tbl_name: str) -> TableAttributes:
    """
    Get column names, types, and schema definition string for a DuckDB table.
    """

    # Query schema
    table_schema = db.sql(f"DESCRIBE SELECT * FROM {tbl_name};").df()
    col_info = table_schema[["column_name", "column_type"]]

    # Build schema string
    schema_str = ", ".join(
        f"{name} {dtype}"
        for name, dtype in zip(col_info["column_name"], col_info["column_type"])
    )

    return TableAttributes(
        col_names=col_info["column_name"].tolist(),
        col_types=col_info["column_type"].tolist(),
        tbl_schema=schema_str,
    )


@dataclass
class SystemPrompt:
    system: str
    schema: str
    col_names: str
    col_types: str
    tbl_name: str


def system_prompt(tbl_name):
    # Get table schema
    tbl_attr = get_tbl_attr(tbl_name=tbl_name)

    # Prompt templates
    system_template = (
        "Given the following SQL table, your job is to write queries given a user’s request. "
        "Return just the SQL query as plain text, without additional text, and don't use markdown format.\n\n"
        f"CREATE TABLE {tbl_name} ({tbl_attr.tbl_schema})\n"
    )
    return SystemPrompt(
        system=system_template,
        schema=tbl_attr.tbl_schema,
        col_names=tbl_attr.col_names,
        col_types=tbl_attr.col_types,
        tbl_name=tbl_name,
    )


def user_prompt(question):
    user_template = f"Write a SQL query that returns: {question}"
    return user_template
