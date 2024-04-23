import marimo

__generated_with = "0.4.0"
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
    mo.md('# Graphic')
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
def __(df_, mo, n, product_filter):
    def make_html_thumb(url):
        return f"""<img src="{url}" width="200"/>"""


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
    return i, make_html_thumb, row, scores, thumbs


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
    images_products[images_products['product'] == product_filter.value]
    return


@app.cell
def __(match_product, mo):
    mo.md(f'# Images of the match product {match_product.value}')
    return


@app.cell
def __(images_products, match_product):
    images_products[images_products['product'] == match_product.value]
    return


@app.cell
def __(match_product, mo):
    mo.md(f'# Images without located objects of the match product {match_product.value}')
    return


@app.cell
def __(data, match_product):
    located_objects = data.get_images_without_located_objects()
    located_objects[located_objects['product'] == match_product.value]
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
    main_objects[main_objects['product'] == match_product.value]
    return main_objects,


@app.cell
def __(match_product, mo):
    mo.md(f'# Matches of the match product {match_product.value}')
    return


@app.cell
def __(data):
    matches = data.get_image_matches()
    # matches[(matches['search_product']==product_filter.value) & (matches['match_product']==match_product.value) & (matches["search_angle"] == matches['match_angle']) & (matches["search_image_type"] == matches['match_image_type'])]
    return matches,


@app.cell
def __(match_product, matches, product_filter):
    matches[(matches['search_product']==product_filter.value) & (matches['match_product']==match_product.value)]
    return


@app.cell
def __():
    # matches[(matches['search_image_id']==115345) & (matches['match_image_id']==115361)]
    return


if __name__ == "__main__":
    app.run()
