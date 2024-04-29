import marimo

__generated_with = "0.4.0"
app = marimo.App(width="full")


@app.cell
def __():
    from multi_image import data, ui
    import marimo as mo
    import pandas as pd

    df = data.get_image_matches()
    return data, df, mo, pd, ui


@app.cell
def __():
    def make_html_thumb(url):
        return f"""<a href="{url}" target="_blank"><img src="{url}" width="200"/></a>"""
    return make_html_thumb,


@app.cell
def __(mo):
    mo.md("# Families")
    return


@app.cell
def __(data):
    families_df = data.get_families()
    return families_df,


@app.cell
def __(families_df, mo):
    family_option = mo.ui.dropdown(
        options=families_df["family"].drop_duplicates().to_list()
    )
    family_option
    return family_option,


@app.cell
def __(families_df, family_option, mo):
    mo.stop(
        family_option.value is None,
        mo.md("# Choose a family"),
    )

    entity_family = families_df.query(f"family=='{family_option.value}'")
    entity_products = entity_family["product"].drop_duplicates().to_list()
    return entity_family, entity_products


@app.cell
def __(df, entity_products):
    entity_matches_df = df[
        df.search_product.isin(entity_products)
        & df.match_product.isin(entity_products)
    ].query(
        "(search_angle == match_angle) and (search_image_type == 'Ghost') and (match_image_type == 'Ghost') and (search_first_sale>='2023-01-01') and (match_first_sale>='2023-01-01')"
    )
    return entity_matches_df,


@app.cell
def __(entity_matches_df, ui):
    family_product_filter = ui.get_product_filter(entity_matches_df)
    family_product_filter
    return family_product_filter,


@app.cell
def __(entity_matches_df, family_product_filter, mo):
    mo.stop(
        family_product_filter.value is None,
        mo.md("# Choose a product"),
    )
    family_df_product = entity_matches_df.query(
        f"search_product == '{family_product_filter.value}'"
    )
    return family_df_product,


@app.cell
def __(family_df_product, pd):
    n = 10
    family_top_n_products = (
        family_df_product.groupby("match_product")
        .image_score.max()
        .sort_values(ascending=False)[:n]
        .index
    )

    family_df_product_top_n = family_df_product[
        family_df_product.match_product.isin(family_top_n_products)
    ].assign(
        match_product=lambda df: pd.Categorical(
            df.match_product, categories=family_top_n_products, ordered=True
        )
    )

    family_df_ = family_df_product_top_n.sort_values("image_score").pivot(
        index=[
            "search_image_type",
            "search_angle",
            "search_product",
            "search_thumb",
        ],
        columns="match_product",
        values=["match_thumb", "image_score"],
    )
    return family_df_, family_df_product_top_n, family_top_n_products, n


@app.cell
def __(family_df_product_top_n):
    means = (
        family_df_product_top_n.groupby("match_product")["image_score"]
        .mean()
        .reset_index()
        .values
    )

    import numpy as np


    def array_to_string(data):
        # Convert the elements of the array to formatted strings
        formatted_elements = [f"{item[0]} ({item[1]:0.2%})" for item in data]

        # Join all formatted elements with " | " and add leading and trailing " | "
        result_string = " | ".join(formatted_elements)

        return result_string
    return array_to_string, means, np


@app.cell
def __(
    array_to_string,
    family_df_,
    family_product_filter,
    family_top_n_products,
    make_html_thumb,
    means,
    mo,
):
    total_top_n_products = len(family_top_n_products)

    _family_header = (
        f"| image_type | angle | {family_product_filter.value} |"
        + array_to_string(means)
        + "|\n"
        + "|---" * (total_top_n_products + 3)
        + "|\n"
    )

    _family_table = _family_header

    for k, row3 in family_df_.iterrows():
        family_thumbs = (
            f"| {k[0]}| {k[1]}| {make_html_thumb(k[3])} |"
            + "|".join(
                row3.loc["match_thumb"]
                .fillna("")
                .map(
                    lambda t: (
                        f"""<a href="{t}" target="_blank"><img src="{t}" width="200" alt="{t}"/></a>"""
                    )
                )
            )
            + "|---" * (total_top_n_products + 3)
            + "|\n"
        )
        family_scores = (
            f"| {k[0]}| {k[1]}|  |"
            + "|".join(row3.loc["image_score"].map(lambda s: f"{s:0.2%}"))
            + "|---" * (total_top_n_products + 3)
            + "|\n"
        )
        _family_table += family_scores
        _family_table += family_thumbs

    mo.md(_family_table)
    return family_scores, family_thumbs, k, row3, total_top_n_products


@app.cell
def __(data):
    images_products = data.get_products_with_their_images()
    return images_products,


@app.cell
def __(family_product_filter, mo):
    mo.md(f"# Images of the search product {family_product_filter.value}")
    return


@app.cell
def __(family_product_filter, images_products):
    images_products[
        (images_products["product"] == family_product_filter.value)
        & (images_products.image_uri.str.contains("ghost", case=False))
    ]
    return


@app.cell
def __(family_df_, ui):
    match_product = ui.get_match_product(family_df_)
    match_product
    return match_product,


@app.cell
def __(match_product, mo):
    mo.md(f"# Images of the match product {match_product.value}")
    return


@app.cell
def __(images_products, match_product):
    images_products[
        (images_products["product"] == match_product.value)
        & (images_products.image_uri.str.contains("ghost", case=False))
    ]
    return


@app.cell
def __(match_product, mo):
    mo.md(f"# Matches of the match product {match_product.value}")
    return


@app.cell
def __(df, family_product_filter, match_product):
    df[
        (df["search_product"] == family_product_filter.value)
        & (df["match_product"] == match_product.value)
        & (df["search_image_type"] == "Ghost")
        & (df["match_image_type"] == "Ghost")
    ]
    return


if __name__ == "__main__":
    app.run()
