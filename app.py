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

    mo.vstack(_image_rows)
    return (
        angle,
        df_available_angles,
        df_product,
        df_product_angle,
        top_n_selected,
    )


if __name__ == "__main__":
    app.run()
