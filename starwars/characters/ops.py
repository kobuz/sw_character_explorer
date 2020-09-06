from typing import Iterator

import petl as etl


def transform(characters: Iterator[dict], planets: Iterator[dict]):
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


def to_csv(data):
    output = etl.MemorySource()
    etl.tocsv(data, output)
    return output.getvalue()


def fetch_and_save():
    from characters import swapi

    cli = swapi.Client("https://swapi.dev/api/")
    characters = cli.characters()
    planets = cli.planets()

    result = transform(characters, planets)
    csv = to_csv(result)
    from characters.models import Collection

    coll = Collection.objects.create()
    from django.core.files.base import ContentFile

    coll.target_file.save("", ContentFile(csv))


def load_table(collection):
    csv = etl.fromcsv(collection.target_file)
    return csv
