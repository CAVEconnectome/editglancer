# Code adapted from Casey Schneider-Mizell's scryingstone repo
from typing import Literal, Union

import pandas as pd
from caveclient import CAVEclient
from nglui import statebuilder
from nglui.easyviewer import EasyViewer

from .utils import (
    assemble_dataframe,
    edit_statebuilder,
    get_operations,
    run_disjoint_roots,
)

ReturnAsType = Literal["url", "viewer", "html", "json", "dict", "shared"]


def get_detailed_operations(root_id: int, client: CAVEclient) -> pd.DataFrame:
    """Get a detailed dataframe of operations for a given root id."""
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
    """Generate a statebuilder object with the current viewer resolution."""
    sb = edit_statebuilder(client, client.info.viewer_resolution())
    return sb


def generate_link_for_root(
    root_id: int, client: CAVEclient, return_as: ReturnAsType = "html"
) -> Union[str, EasyViewer, str, dict]:
    """Generate a neuroglancer link showing edit information for a given root id.

    Parameters
    ----------
    root_id :
        The root id in a segmentation to generate the link for.
    client :
        The CAVE client object to use for the link generation.
    return_as :
        Choice of output type. One of ['url', 'viewer', 'html', 'json', 'dict', 'shared']
        Note that if a viewer is returned, the state is not reset.
            "url" : Returns the raw url describing the state
            "viewer" : Returns an nglui.easyviewer.EasyViewer object holding the state
            "html" : Returns an HTML link to the url, useful for notebooks.
            "json" : Returns a JSON string describing the state.
            "dict" : Returns a dict version of the JSON state.

    Returns
    -------
    :
        The neuroglancer link for the given root id. The type of the output is
        determined by the `return_as` parameter.
    """
    op_df = get_detailed_operations(root_id, client)
    sb = generate_statebuilder(client)
    return sb.render_state(op_df, return_as=return_as)
