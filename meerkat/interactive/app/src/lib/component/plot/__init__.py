from pydantic import Field

from meerkat.dataframe import DataFrame
from meerkat.interactive.endpoint import Endpoint
from meerkat.interactive.graph import Store

from ..abstract import AutoComponent


def is_none(x):
    return (isinstance(x, Store) and x.__wrapped__ is None) or x is None


class Plot(AutoComponent):
    # name: str = "Plot"

    df: "DataFrame"
    x: str
    y: str
    x_label: str = None
    y_label: str = None
    type: str = Store("scatter")
    slot: str = None
    keys_to_remove: list =  Field(default_factory=list)
    metadata_columns: list = Field(default_factory=list)

    on_select: Endpoint = None

