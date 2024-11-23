
import dash
from dash import dcc, html, Input, Output, State
import json
from main import generate_profile_summary_and_facts_single_step  # Replace with the actual import path

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "DataSense LinkedIn Search"

# App Layout
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f3f6f9",
        "padding": "20px",
        "color": "#333",
    },
    children=[
        # Header
        html.Div(
            style={
                "backgroundColor": "#0077B5",
                "padding": "20px",
                "borderRadius": "10px",
                "textAlign": "center",
                "color": "white",
            },
            children=[
                html.H1("🔍 DataSense LinkedIn Search"),
                html.H4("Explore LinkedIn Profiles Seamlessly"),
            ],
        ),
        # Input Section
        html.Div(
            style={"marginTop": "30px"},
            children=[
                html.Label(
                    "Enter Full Name:", style={"fontSize": "18px", "fontWeight": "bold"}
                ),
                dcc.Input(
                    id="name-input",
                    type="text",
                    placeholder="E.g., Shagun Nagpal",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "fontSize": "16px",
                        "borderRadius": "5px",
                        "border": "1px solid #ccc",
                    },
                ),
                html.Button(
                    "Search Profile 🔎",
                    id="search-button",
                    style={
                        "marginTop": "10px",
                        "padding": "10px 20px",
                        "fontSize": "16px",
                        "borderRadius": "5px",
                        "backgroundColor": "#0077B5",
                        "color": "white",
                        "border": "none",
                    },
                ),
            ],
        ),
        # Profile Picture
        html.Div(id="profile-pic", style={"marginTop": "30px", "textAlign": "center"}),
        # Summary Box
        html.Div(
            id="summary-box",
            style={
                "marginTop": "20px",
                "padding": "20px",
                "backgroundColor": "white",
                "border": "1px solid #ddd",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
            },
        ),
        # Interesting Facts Box
        html.Div(
            id="facts-box",
            style={
                "marginTop": "20px",
                "padding": "20px",
                "backgroundColor": "white",
                "border": "1px solid #ddd",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
            },
        ),
        # Loading Indicator
        dcc.Loading(
            id="loading-spinner",
            type="circle",
            children=[
                html.Div(
                    id="loading-placeholder",
                    style={"marginTop": "20px", "textAlign": "center"},
                )
            ],
        ),
    ],
)

# Callback to fetch and display the results
@app.callback(
    [Output("profile-pic", "children"), Output("summary-box", "children"), Output("facts-box", "children")],
    [Input("search-button", "n_clicks")],
    [State("name-input", "value")],
)
def display_profile_data(n_clicks, name):
    if n_clicks is None or not name:
        return ["", "", ""]

    try:
        # Display loading spinner
        spinner = html.Div("Generating insights... Please wait. ⏳")

        # Fetch data using the function
        result = generate_profile_summary_and_facts_single_step(name)
        data = json.loads(result)  # Ensure JSON parsing

        # Extract data
        profile_pic_url = data.get("profile_pic_url", "")
        summary = data.get("summary", "No summary available.")
        interesting_facts = data.get("interesting_facts", [])

        # Format outputs
        profile_pic_section = html.Img(
            src=profile_pic_url,
            style={
                "borderRadius": "50%",
                "width": "150px",
                "height": "150px",
                "marginBottom": "20px",
                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
            },
        )

        summary_section = html.Div(
            children=[
                html.H3("📋 Profile Summary", style={"color": "#0077B5"}),
                html.P(summary, style={"fontSize": "16px", "lineHeight": "1.5"}),
            ]
        )

        facts_section = html.Div(
            children=[
                html.H3("✨ Interesting Facts", style={"color": "#0077B5"}),
                html.Ul([html.Li(fact, style={"fontSize": "16px"}) for fact in interesting_facts]),
            ]
        )

        return profile_pic_section, summary_section, facts_section

    except Exception as e:
        error_msg = html.Div(
            children=[
                html.H3("⚠️ Error Occurred", style={"color": "red"}),
                html.P(f"An error occurred while fetching the data: {str(e)}"),
            ],
            style={"color": "red", "fontSize": "16px"},
        )
        return ["", error_msg, ""]


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
