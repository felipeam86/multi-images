from pathlib import Path
import os

import pandas as pd
from cachesql import Database
from dotenv import load_dotenv

load_dotenv()
db_dwh = Database(uri=os.getenv("POSTGRES_URL"))  # datawarehouse

QUERIES_FOLDER = Path(__file__).parent / "queries"


def get_image_matches() -> pd.DataFrame:
    query = Path(QUERIES_FOLDER / "get_image_matches.sql").read_text()
    df = (
        db_dwh.query(query)
        .sort_values(
            ["search_product", "search_thumb", "image_score"],
            ascending=False,
        )
        .assign(
            match_thumb=lambda df: df["match_thumb"].str.replace(
                "gs://", "https://storage.googleapis.com/"
            ),
            search_thumb=lambda df: df["search_thumb"].str.replace(
                "gs://", "https://storage.googleapis.com/"
            ),
        )
    )
    return df
