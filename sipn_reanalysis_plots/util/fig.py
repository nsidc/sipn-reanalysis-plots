import base64
import contextlib
from io import BytesIO
from typing import Literal

from matplotlib.figure import Figure


def fig_to_high_and_lowres_base64(
    fig: Figure,
) -> tuple[str, str]:
    return (
        _fig_to_base64(fig),
        _fig_to_base64(fig, dpi=600),
    )


def _fig_to_base64(
    fig: Figure,
    *,
    dpi: int | float | Literal['figure'] = 'figure',
) -> str:
    """Convert figure to base64 string for HTML embedding."""
    with contextlib.closing(BytesIO()) as buf:
        fig.savefig(buf, format='png', dpi=dpi)
        img_bytes = base64.b64encode(buf.getbuffer()).decode('ascii')

    return img_bytes
