import dash_html_components as html
import plotly.express as px


def make_line(df, title="Global"):
    fig = px.line(
        df,
        title=title,
        x="날짜",
        y=["확진자 수", "사망자 수", "완치자 수"],
        template="plotly_dark",
        labels={"value": "합계", "variable": "구분", "date": "일자"},
        hover_data={"value": ":,", "variable": False, "날짜": False},
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig


def make_bar(df, conditions):
    fig = px.bar(
        df,
        x="구분",
        y="합계",
        hover_data={"합계": ":,"},
        template="plotly_dark",
        title="Total Global Cases",
        labels={"condition": "구분", "count": "합계", "color": "구분"},
    )
    return fig


def make_map(df):
    fig = px.scatter_geo(
        df,
        text="사망자 수",
        color="확진자 수",
        locations="국가 구분",
        locationmode="country names",
        hover_name="국가 구분",
        size="확진자 수",
        size_max=50,
        hover_data={"확진자 수": ":,2f", "완치자 수": ":,2f", "사망자 수": ":,2f", "국가 구분": False},
        template="plotly_dark",
        projection="orthographic",
    )
    return fig


def make_table(df):
    return html.Table(
        children=[
            html.Thead(
                style={"display": "block", "margin": "25px 0px"},
                children=[
                    html.Tr(
                        children=[html.Th(column_name) for column_name in df.columns],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4,1fr)",
                            "fontWeight": "600",
                            "fontSize": 16,
                        },
                    )
                ],
            ),
            html.Tbody(
                style={"maxHeight": "50vh", "display": "block", "overflow": "scroll"},
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4,1fr)",
                            "border-top": "1px solid white",
                            "padding": "30px 0px",
                            "text-align": "center",
                        },
                        children=[html.Td(value_column) for value_column in value],
                    )
                    for value in df.values
                ],
            ),
        ]
    )
