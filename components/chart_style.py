from typing import Callable
from components.colors import NEUTRAL_COLOR_SEQUENCE

def standard_chart_style(_func=None, *, tickformat: str = ".2~s", texttemplate: str | None = None):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # call the original chart‐builder
            fig = func(*args, **kwargs)

            # preserve any existing axis config
            x_existing = fig.layout.xaxis.to_plotly_json() if fig.layout.xaxis else {}
            y_existing = fig.layout.yaxis.to_plotly_json() if fig.layout.yaxis else {}

            # rebuild x-axis style
            xaxis_style = {
                "showline": True, "linewidth": 1, "mirror": True,
                "ticks": "outside", "ticklen": 6, "fixedrange": True,
                "showgrid": False, "zeroline": False,
                "title_standoff": 15,
                "showticklabels": x_existing.get("showticklabels", False),
                "title": {
                    "text": x_existing.get("title", {}).get("text", None),
                    "standoff": 15
                }
            }

            # rebuild y-axis style with SI tickformat
            yaxis_style = {
                "showline": True, "linewidth": 1, "mirror": True,
                "ticks": "outside", "ticklen": 6, "fixedrange": False,
                "showgrid": True, "gridcolor": "#e5e5e5", "gridwidth": 1,
                "zeroline": False,
                "title_standoff": 15,
                "showticklabels": y_existing.get("showticklabels", True),
                "title": {
                    "text": y_existing.get("title", {}).get("text", None),
                    "standoff": 15
                },
                "tickformat": tickformat
            }

            # apply the overall layout
            fig.update_layout(
                font=dict(family="Arial", size=10),
                margin=dict(t=40, b=20, l=20, r=20),
                plot_bgcolor="white",
                xaxis=xaxis_style,
                yaxis=yaxis_style,
                colorway=NEUTRAL_COLOR_SEQUENCE,
                legend=dict(
                    orientation="h",
                    yanchor="bottom", y=1.02,
                    xanchor="right", x=1,
                    title_text="", font_size=10
                ),
                hoverlabel=dict(
                    bgcolor="white", font_size=12, bordercolor="#cccccc"
                ),
                dragmode=False,
                title=None
            )

            # determine base font size and texttemplate
            base_font_size = fig.layout.font.size or 12
            fmt = texttemplate or f"%{{text:{tickformat}}}"

            # format on-chart labels
            fig.update_traces(
                texttemplate=fmt,
                textposition="outside",
                cliponaxis=False,
                textfont=dict(size=base_font_size)
            )

            return fig

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)



from functools import wraps

def status_chart_style(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)

        # Preserve any existing axis titles/tick settings
        x_existing = fig.layout.xaxis.to_plotly_json() if fig.layout.xaxis else {}
        y_existing = fig.layout.yaxis.to_plotly_json() if fig.layout.yaxis else {}

        xaxis_style = {
            "title": x_existing.get("title", {}).get("text", None),
            "title_standoff": 15,
            "showline": True,
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
            "ticklen": 6,
            "fixedrange": True,
            "showgrid": True,
            "gridcolor": "#e5e5e5",
            "gridwidth": 1,
            "zeroline": False,
        }

        yaxis_style = {
            "title": None,
            "title_standoff": 15,
            "showline": True,
            "linewidth": 1,
            "mirror": True,
            "ticks": "outside",
            "ticklen": 6,
            "fixedrange": True,
            "showgrid": True,
            "gridcolor": "#e5e5e5",
            "gridwidth": 1,
            "zeroline": False,
            "showticklabels": y_existing.get("showticklabels", True),
            "tickformat": ",.0f"
        }

        fig.update_layout(
            font=dict(family="Arial", size=10),
            margin=dict(t=60, b=20, l=20, r=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=xaxis_style,
            yaxis=yaxis_style,
            colorway=NEUTRAL_COLOR_SEQUENCE,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.0,
                xanchor="right",
                x=1.0,
                title_text="",
                font_size=10
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                bordercolor="#cccccc"
            ),
            dragmode=False,
            title=None
        )

        return fig

    return wrapper



from functools import wraps
from typing import Callable
import pandas as pd
from components.colors import NEUTRAL_COLOR_SEQUENCE

def stacked_bar_chart_style(
        x_col="x",
        y_col="y",
        *,
        tickformat: str = ".2s",
        total_formatter: Callable[[float], str] | None = None,
        annotation_font_size: int = 10,
):
    if total_formatter is None:
        def total_formatter(v: float) -> str:
            num = float(v)
            for unit in ("", "k", "M", "B", "T"):
                if abs(num) < 1000:
                    return f"{num:.0f}{unit}" if unit == "" else f"{num:.1f}{unit}"
                num /= 1000.0
            return f"{num:.1f}E"

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fig, df = func(*args, **kwargs)

            # preserve order if categorical
            categoryarray = (
                df[x_col].cat.categories.tolist()
                if pd.api.types.is_categorical_dtype(df[x_col])
                else None
            )

            fig.update_layout(
                autosize=True,
                margin=dict(l=0, r=0, t=0, b=0),
                font=dict(family="Arial", size=10),
                plot_bgcolor="white",
                paper_bgcolor="white",
                colorway=NEUTRAL_COLOR_SEQUENCE,
                barmode="stack",
                xaxis=dict(
                    showline=True, linewidth=1, mirror=True,
                    ticks="outside", ticklen=6, fixedrange=False,  # allow click interactivity
                    showgrid=False, zeroline=False, showticklabels=True,
                    title_standoff=15,
                    categoryorder="array" if categoryarray else "trace",
                    categoryarray=categoryarray,
                ),
                yaxis=dict(
                    showline=True, linewidth=1, mirror=True,
                    ticks="outside", ticklen=6, fixedrange=False,
                    showgrid=True, gridcolor="#e5e5e5", gridwidth=1,
                    zeroline=False, title_standoff=15,
                    tickformat=tickformat
                ),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, title_text="", font_size=10
                ),
                hoverlabel=dict(bgcolor="white", font_size=12, bordercolor="#cccccc"),
                dragmode=False,
                title=None,
            )

            # Set hover and click data visibility
            fig.update_traces(
                text=None,
                hoverinfo="x+y+name",
                hovertemplate="%{y:,}<extra>%{fullData.name}</extra>",
            )

            # Add annotation with totals above each bar group
            totals = df.groupby(x_col)[y_col].sum().reset_index()
            for _, row in totals.iterrows():
                formatted = total_formatter(row[y_col])
                fig.add_annotation(
                    x=row[x_col],
                    y=row[y_col],
                    text=formatted,
                    showarrow=False,
                    yshift=5,
                    font=dict(size=annotation_font_size),
                )

            return fig

        return wrapper

    return decorator


