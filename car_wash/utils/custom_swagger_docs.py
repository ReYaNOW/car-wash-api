import json

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import swagger_ui_default_parameters
from fastapi.responses import HTMLResponse

tags_metadata = [
    {
        'name': 'JWT',
        'description': 'Operations with **jwt tokens** and **users**.',
    },
    {
        'name': 'Users',
        'description': 'and its attributes ' '(**roles**)',
    },
    {
        'name': 'CarWashes',
        'description': 'and its attributes '
        '(**locations, schedules, bookings**)',
    },
    {
        'name': 'Cars',
        'description': 'and its attributes '
        '(**brands, models, generations, body_types, configurations**)',
    },
]


def custom_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_favicon_url: str = 'https://fastapi.tiangolo.com/img/favicon.png',
) -> HTMLResponse:
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()

    prms = ''
    for key, value in current_swagger_ui_parameters.items():
        prms += f'{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n'

    return HTMLResponse(
        f"""
        <!doctype html>
        <html>
          <head>
            <script src=
            "https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"
            ></script>
            <script src=
            "https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js"
            ></script>

            <!-- "Hierarchical Tags" -->
            <script src="
            https://unpkg.com/swagger-ui-plugin-hierarchical-tags
            "></script>

            <link rel="stylesheet" type="text/css" href="
            https://unpkg.com/swagger-ui-dist/swagger-ui.css
            " />

            <title>{title}</title>
            <link rel="icon" href="{swagger_favicon_url}">
            <style>
              body {{ margin: 0; }}
            </style>
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script>
              window.onload = function() {{
                const ui = SwaggerUIBundle({{
                  url: '{openapi_url}',
                  {prms}
                  persistAuthorization: true,
                  defaultModelsExpandDepth: 0,
                  presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                  ],
                  plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl,
                    HierarchicalTagsPlugin
                  ],
                  hierarchicalTagSeparator: /[:|]/
                }});
                window.ui = ui;
              }};
            </script>
          </body>
        </html>
        """
    )


def create_custom_swagger_docs(app: FastAPI) -> None:
    @app.get('/docs', include_in_schema=False)
    async def custom_swagger_ui() -> HTMLResponse:
        # Pycharm linter cant find openapi_url and title
        if hasattr(app, 'openapi_url') and hasattr(app, 'title'):
            return custom_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title,
            )
