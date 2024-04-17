import marimo as mo


def make_html_thumb(url):
    return f"""<img src="{url}" width="200"/>"""


def get_product_filter(df):
    return mo.ui.dropdown(
        options=df.search_product.sort_values().drop_duplicates().tolist(),
    )


def make_thumbnail_row(df_product_angle, n=10):
    return mo.md(
        "|"
        + df_product_angle.iloc[0]["search_title"]
        + "|"
        + "|".join(df_product_angle[:n]["match_title"])
        + "|\n"
        + "|---" * (n + 1)
        + "|\n"
        + "|"
        + f"""<img src="{df_product_angle.iloc[0]["search_thumb"]}" width="200"/>"""
        + "|"
        + "|".join(
            df_product_angle[:n]["match_thumb"].map(lambda t: make_html_thumb(t))
        )
        + "|\n"
    )
