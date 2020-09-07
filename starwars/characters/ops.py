from dataclasses import dataclass
from typing import Iterator, Tuple, Optional

import petl as etl
from petl import Table

from . import swapi


@dataclass
class TableData:
    header: Tuple[str]
    data: Table
    next_limit: Optional[int]


def transform(characters: Iterator[dict], planets: Iterator[dict]) -> Table:
    planets_table = (
        etl.fromdicts(planets)
        .addfield("id", lambda row: row.url.split("/")[-2])
        .rename("name", "planet_name")
        .cut("id", "planet_name")
    )
    characters_table = (
        etl.fromdicts(characters)
        .addfield("date", lambda row: row.edited.split("T")[0])
        .convert("homeworld", lambda hw: hw.split("/")[-2])
        .join(planets_table, lkey="homeworld", rkey="id")
        .cutout("homeworld")
        .rename("planet_name", "homeworld")
        .cutout("films", "species", "vehicles", "starships", "created", "edited", "url")
    )

    return characters_table


def to_csv(data: Table) -> bytes:
    output = etl.MemorySource()
    etl.tocsv(data, output)
    return output.getvalue()


def fetch_data_into_csv() -> bytes:
    client = swapi.make_client()
    characters = client.characters()
    planets = client.planets()

    result = transform(characters, planets)
    csv = to_csv(result)
    return csv


def load_table_data(csv_file, limit) -> TableData:
    table = etl.fromcsv(csv_file)
    return TableData(
        header=etl.header(table),
        data=etl.data(table, limit),
        next_limit=limit + 10 if limit < table.len() else None,
    )


def load_grouped_data(csv_file, fields) -> TableData:
    table = etl.fromcsv(csv_file)
    if len(fields) == 1:
        fields = fields[0]
    return TableData(
        header=etl.header(table),
        data=etl.aggregate(table, key=fields, aggregation=len),
        next_limit=None,
    )
