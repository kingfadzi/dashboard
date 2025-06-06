# components/react_select_dropdown.py

from dash_extensions import ReactComponent
import dash_bootstrap_components as dbc

def render_language_filter():
    return dbc.Col(
        ReactComponent(
            id="language-filter",
            module="react-select",
            props={
                "isMulti": True,
                "placeholder": "Select Language(s)",
                "className": "react-select-container",
                "classNamePrefix": "react-select",
                "closeMenuOnSelect": False,
                "hideSelectedOptions": False,
                "components": {
                    "MultiValue": {
                        "custom": True,
                        "function": """
                            (props) => {
                                const max = 2;
                                const index = props.selectProps.value.findIndex(v => v.value === props.data.value);
                                const visible = index < max;
                                const total = props.selectProps.value.length;

                                if (visible) {
                                    return window.React.createElement(
                                        window.Select.components.MultiValue,
                                        props
                                    );
                                } else if (index === max) {
                                    return window.React.createElement(
                                        "div",
                                        {
                                            style: {
                                                padding: "2px 8px",
                                                fontSize: "0.75rem",
                                                backgroundColor: "#ddd",
                                                borderRadius: "4px",
                                                margin: "2px",
                                            }
                                        },
                                        `+${total - max} more`
                                    );
                                } else {
                                    return null;
                                }
                            }
                        """
                    }
                },
                "styles": {
                    "control": {"fontSize": "14px", "minHeight": "38px"},
                    "multiValue": {"maxWidth": "90px"},
                    "multiValueLabel": {"overflow": "hidden", "textOverflow": "ellipsis"}
                }
            }
        ),
        width=2
    )
