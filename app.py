import marimo

__generated_with = "0.4.4"
app = marimo.App(width="full")


@app.cell
def __():
    from multi_image import data, ui
    import marimo as mo

    df = data.get_image_matches()
    product_filter = ui.get_product_filter(df)
    return data, df, mo, product_filter, ui


@app.cell
def __(product_filter):
    product_filter
    return


@app.cell
def __(df, mo, product_filter, ui):
    mo.stop(
        product_filter.value is None,
        mo.md("# Choose a product"),
    )
    df_product = df.query(f"search_product == '{product_filter.value}'")
    df_available_angles = (
        df_product[["search_angle", "search_image_type"]]
        .drop_duplicates()
        .iterrows()
    )
    _image_rows = []
    for _, angle in df_available_angles:
        df_product_angle = df_product.query(
            f"(search_angle == '{angle.search_angle}') and (search_image_type == '{angle.search_image_type}')"
        )

        top_n_selected = ui.make_thumbnail_row(df_product_angle, n=10)
        _image_rows.append(top_n_selected)

    # mo.vstack(_image_rows)
    return (
        angle,
        df_available_angles,
        df_product,
        df_product_angle,
        top_n_selected,
    )


@app.cell
def __(mo):
    mo.md("# Graphic")
    return


@app.cell
def __(df_product):
    n = 10
    top_n_products = (
        df_product.groupby("match_product")
        .image_score.max()
        .sort_values(ascending=False)[:n]
        .index
    )
    df_product_top_n = df_product[
        df_product.match_product.isin(top_n_products)
    ].query(
        "(search_angle == match_angle) and (search_image_type == match_image_type)"
    )
    df_ = df_product_top_n.pivot(
        index=[
            "search_image_type",
            "search_angle",
            "search_product",
            "search_thumb",
        ],
        columns="match_product",
        values=["match_thumb", "image_score"],
    )
    return df_, df_product_top_n, n, top_n_products


@app.cell
def __():
    def make_html_thumb(url):
        return f"""<a href="{url}" target="_blank"><img src="{url}" width="200"/></a>"""
    return make_html_thumb,


@app.cell
def __(df_, make_html_thumb, mo, n, product_filter):
    _header = (
        f"| image_type | angle | {product_filter.value} |"
        + "|".join(df_.columns.levels[1])
        + "|\n"
        + "|---" * (n + 3)
        + "|\n"
    )

    _table = _header

    for i, row in df_.iterrows():
        thumbs = (
            f"| {i[0]}| {i[1]}| {make_html_thumb(i[3])} |"
            + "|".join(
                row.loc["match_thumb"]
                .fillna("")
                .map(lambda t: f"""<img src="{t}" width="200"/>""")
            )
            + "|---" * (n + 3)
            + "|\n"
        )
        scores = (
            f"| {i[0]}| {i[1]}|  |"
            + "|".join(row.loc["image_score"].map(lambda s: f"{s:0.2%}"))
            + "|---" * (n + 3)
            + "|\n"
        )
        _table += scores
        _table += thumbs

    mo.md(_table)
    return i, row, scores, thumbs


@app.cell
def __(df_, ui):
    match_product = ui.get_match_product(df_)
    match_product
    return match_product,


@app.cell
def __(data):
    images_products = data.get_products_with_their_images()
    return images_products,


@app.cell
def __(mo, product_filter):
    mo.md(f"# Images of the search product {product_filter.value}")
    return


@app.cell
def __(images_products, product_filter):
    images_products[images_products["product"] == product_filter.value]
    return


@app.cell
def __(match_product, mo):
    mo.md(f"# Images of the match product {match_product.value}")
    return


@app.cell
def __(images_products, match_product):
    images_products[images_products["product"] == match_product.value]
    return


@app.cell
def __(match_product, mo):
    mo.md(
        f"# Images without located objects of the match product {match_product.value}"
    )
    return


@app.cell
def __(data, match_product):
    located_objects = data.get_images_without_located_objects()
    located_objects[located_objects["product"] == match_product.value]
    return located_objects,


@app.cell
def __(match_product, mo):
    mo.md(
        f"""
        # Images without main object of the match product {match_product.value}.\n
        These images are not inside the product set
        """
    )
    return


@app.cell
def __(data, match_product):
    main_objects = data.get_images_without_main_object()
    main_objects[main_objects["product"] == match_product.value]
    return main_objects,


@app.cell
def __(match_product, mo):
    mo.md(f"# Matches of the match product {match_product.value}")
    return


@app.cell
def __(data):
    matches = data.get_image_matches()
    # matches[(matches['search_product']==product_filter.value) & (matches['match_product']==match_product.value) & (matches["search_angle"] == matches['match_angle']) & (matches["search_image_type"] == matches['match_image_type'])]
    return matches,


@app.cell
def __(match_product, matches, product_filter):
    matches[
        (matches["search_product"] == product_filter.value)
        & (matches["match_product"] == match_product.value)
    ]
    return


@app.cell
def __(mo):
    mo.md("# Cosine similarity")
    return


@app.cell
def __(data):
    import pandas as pd

    df_embeddings = data.get_image_embeddings()

    df_embeddings_search = (
        df_embeddings.query("group == 'search'")
        .set_index("image_id")
        .rename_axis(index="search_image_id")
        .embedding.apply(pd.Series)
    )
    df_embeddings_match = (
        df_embeddings.query("group == 'match'")
        .set_index("image_id")
        .rename_axis(index="match_image_id")
        .embedding.apply(pd.Series)
    )
    return df_embeddings, df_embeddings_match, df_embeddings_search, pd


@app.cell
def __(df_embeddings_match, df_embeddings_search, pd):
    from sklearn.metrics.pairwise import cosine_similarity

    df_sim = pd.DataFrame(
        data=cosine_similarity(df_embeddings_search, df_embeddings_match),
        index=df_embeddings_search.index,
        columns=df_embeddings_match.index,
    )
    return cosine_similarity, df_sim


@app.cell
def __(df_sim):
    df_sim
    return


@app.cell
def __(df_embeddings, df_sim, ui):
    df_melted_sim = df_sim.assign(search_image_id=df_sim.index).melt(
        id_vars="search_image_id",
        var_name="match_image_id",
        value_name="image_score",
    )

    df_search_data = df_embeddings.query("group=='search'")[
        ["product", "image_id", "image_url", "angle", "image_type"]
    ].rename(
        columns={
            "product": "search_product",
            "image_id": "search_image_id",
            "image_url": "search_image_url",
            "angle": "search_angle",
            "image_type": "search_image_type",
        }
    )

    df_match_data = df_embeddings.query("group=='match'")[
        ["product", "image_id", "image_url", "angle", "image_type"]
    ].rename(
        columns={
            "product": "match_product",
            "image_id": "match_image_id",
            "image_url": "match_image_url",
            "angle": "match_angle",
            "image_type": "match_image_type",
        }
    )

    df_merged = (
        df_melted_sim.merge(df_search_data, on="search_image_id")
        .merge(df_match_data, on="match_image_id")
        .sort_values(
            ["search_product", "image_score"],
            ascending=False,
        )
        .query(
            "(search_angle == match_angle) and (search_image_type == match_image_type)"
        )
    )

    df_merged = df_merged[
        [
            "search_image_id",
            "search_product",
            "match_image_id",
            "match_product",
            "search_image_url",
            "match_image_url",
            "search_angle",
            "match_angle",
            "search_image_type",
            "match_image_type",
            "image_score",
        ]
    ]

    cosine_product_filter = ui.get_product_filter(df_merged)
    return (
        cosine_product_filter,
        df_match_data,
        df_melted_sim,
        df_merged,
        df_search_data,
    )


@app.cell
def __(cosine_product_filter):
    cosine_product_filter
    return


@app.cell
def __(cosine_product_filter, df_merged, mo):
    mo.stop(
        cosine_product_filter.value is None,
        mo.md("# Choose a product"),
    )
    cosine_df_product = df_merged.query(
        f"search_product == '{cosine_product_filter.value}'"
    )
    return cosine_df_product,


@app.cell
def __(cosine_df_product, n):
    cosine_top_n_products = (
        cosine_df_product.groupby("match_product")
        .image_score.max()
        .sort_values(ascending=False)[:n]
        .index
    )
    cosine_df_product_top_n = cosine_df_product[
        cosine_df_product.match_product.isin(cosine_top_n_products)
    ].query(
        "(search_angle == match_angle) and (search_image_type == match_image_type)"
    )
    cosine_df_ = cosine_df_product_top_n.pivot(
        index=[
            "search_image_type",
            "search_angle",
            "search_product",
            "search_image_url",
        ],
        columns="match_product",
        values=["match_image_url", "image_score"],
    )
    return cosine_df_, cosine_df_product_top_n, cosine_top_n_products


@app.cell
def __(cosine_df_, cosine_product_filter, make_html_thumb, mo, n):
    _cosine_header = (
        f"| image_type | angle | {cosine_product_filter.value} |"
        + "|".join(cosine_df_.columns.levels[1])
        + "|\n"
        + "|---" * (n + 3)
        + "|\n"
    )

    _cosine_table = _cosine_header

    for j, row2 in cosine_df_.iterrows():
        cosine_thumbs = (
            f"| {j[0]}| {j[1]}| {make_html_thumb(j[3])} |"
            + "|".join(
                row2.loc["match_image_url"]
                .fillna("")
                .map(lambda t: f"""<img src="{t}" width="200"/>""")
            )
            + "|---" * (n + 3)
            + "|\n"
        )
        cosine_scores = (
            f"| {j[0]}| {j[1]}|  |"
            + "|".join(row2.loc["image_score"].map(lambda s: f"{s:0.2%}"))
            + "|---" * (n + 3)
            + "|\n"
        )
        _cosine_table += cosine_scores
        _cosine_table += cosine_thumbs

    mo.md(_cosine_table)
    return cosine_scores, cosine_thumbs, j, row2


@app.cell
def __(cosine_df_, ui):
    cosine_match_product = ui.get_match_product(cosine_df_)
    cosine_match_product
    return cosine_match_product,


@app.cell
def __(match_product, mo):
    mo.md(f"# Images of the match product {match_product.value}")
    return


@app.cell
def __(cosine_match_product, images_products):
    images_products[images_products["product"] == cosine_match_product.value]
    return


@app.cell
def __(match_product, mo):
    mo.md(
        f"# Images without located objects of the match product {match_product.value}"
    )
    return


@app.cell
def __(cosine_match_product, located_objects):
    located_objects[located_objects["product"] == cosine_match_product.value]
    return


@app.cell
def __(match_product, mo):
    mo.md(
        f"""
        # Images without main object of the match product {match_product.value}.\n
        These images are not inside the product set
        """
    )
    return


@app.cell
def __(cosine_match_product, main_objects):
    main_objects[main_objects["product"] == cosine_match_product.value]
    return


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
        "(search_angle == match_angle) and (search_image_type == match_image_type) and (search_image_type == 'Ghost') and (search_first_sale>='2023-01-01') and (match_first_sale>='2023-01-01')"
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
def __(family_df_product, n, pd):
    family_top_n_products = (
        family_df_product.groupby("match_product")
        .image_score.max()
        .sort_values(ascending=False)[:n]
        .index
    )
    family_df_product_top_n = (
        family_df_product[
            family_df_product.match_product.isin(family_top_n_products)
        ]
        .assign(
            match_product=lambda df: pd.Categorical(
                df.match_product, categories=family_top_n_products, ordered=True
            )
        )
    )

    # family_df_product_top_n_2 = pd.concat(
    #     [
    #         family_df_product_top_n,
    #         family_df_product_top_n.groupby(["search_product", "match_product"])[
    #             ["image_score"]
    #         ]
    #         .mean()
    #         .assign(search_angle="mean")
    #         .reset_index(),
    #     ]
    # )

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
    return family_df_, family_df_product_top_n, family_top_n_products


@app.cell
def __(family_df_product_top_n):
    means = family_df_product_top_n.groupby("match_product")["image_score"].mean().reset_index().values

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
    make_html_thumb,
    means,
    mo,
    n,
):
    _family_header = (
        f"| image_type | angle | {family_product_filter.value} |"
        + array_to_string(means)
        + "|\n"
        + "|---" * (n + 3)
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
            + "|---" * (n + 3)
            + "|\n"
        )
        family_scores = (
            f"| {k[0]}| {k[1]}|  |"
            + "|".join(row3.loc["image_score"].map(lambda s: f"{s:0.2%}"))
            + "|---" * (n + 3)
            + "|\n"
        )
        _family_table += family_scores
        _family_table += family_thumbs

    mo.md(_family_table)
    return family_scores, family_thumbs, k, row3


if __name__ == "__main__":
    app.run()
