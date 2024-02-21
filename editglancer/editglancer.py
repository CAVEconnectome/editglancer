# Code adapted from Casey Schneider-Mizell's scryingstone repo
import pandas as pd
from caveclient import CAVEclient
from nglui import statebuilder

from .utils import (
    assemble_dataframe,
    edit_statebuilder,
    get_operations,
    run_disjoint_roots,
)


def get_detailed_operations(root_id: int, client: CAVEclient) -> pd.DataFrame:
    operations = get_operations(root_id, client)

    operations_df = assemble_dataframe(
        root_id,
        operations,
        client.chunkedgraph.base_resolution,
        client.info.viewer_resolution(),
    )

    operations_df["disjoint_roots"] = run_disjoint_roots(operations_df, client)

    return operations_df


def generate_statebuilder(client: CAVEclient) -> statebuilder.StateBuilder:
    sb = edit_statebuilder(client, client.info.viewer_resolution())
    return sb


def generate_link_for_root(root_id: int, client: CAVEclient, return_as: str = "html"):
    op_df = get_detailed_operations(root_id, client)
    sb = generate_statebuilder(root_id, client)
    return sb.render_state(op_df, return_as=return_as)
