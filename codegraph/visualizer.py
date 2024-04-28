import os
import random
from typing import Dict

import dash
import dash_cytoscape as cyto
import networkx as nx
from dash import html, Input, Output, State, dcc
from dash.dependencies import MATCH
from dash.exceptions import PreventUpdate
import time


def process_module_in_graph(module: Dict[str, list], module_links: list, G: nx.DiGraph):
    module_color = f'#{"".join([random.choice("0123456789ABCDEF") for _ in range(6)])}'

    _module = os.path.basename(module)

    G.add_node(_module, module=module_color)
    for entity in module_links:
        # Add the entity node with the 'module' attribute
        G.add_node(entity, module=module_color)

        for dep in module_links[entity]:
            if "." in dep:
                dep = dep.split(".")[1].replace(".", ".py")

            # Add the dependency node with the 'module' attribute
            G.add_node(dep, module=module_color)

            # Add an edge from the entity to its dependency
            G.add_edge(entity, dep)


def draw_graph(modules_entities: Dict) -> None:
    G = nx.DiGraph()

    for module in modules_entities:
        process_module_in_graph(module, modules_entities[module], G)

    # Convert the nodes and edges to the format required by dash_cytoscape
    elements = [{'data': {'id': node, 'label': node, 'module': data['module']}} for node, data in G.nodes(data=True)]
    elements += [{'data': {'source': edge[0], 'target': edge[1]}} for edge in G.edges()]

    app = dash.Dash(__name__)
    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            elements=elements,
            layout={'name': 'cose', 'nodeRepulsion': 400000, 'idealEdgeLength': 100, 'edgeElasticity': 100, 'timestamp': time.time()},
            style={'width': '100%', 'height': '1200px'},
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'background-color': 'data(module)',
                        'width': '100px',
                        'height': '100px'
                    }
                }
            ]
        ),
        dcc.Store(id='removed_node'),
        html.Div(id='output')
    ])

    @app.callback(
        Output('cytoscape', 'elements'),
        Output('cytoscape', 'layout'),
        Input('removed_node', 'data'),
        State('cytoscape', 'elements'),
        State('cytoscape', 'layout')
    )
    def remove_node(removed_node, elements, layout):
        if removed_node is not None:
            elements = [element for element in elements if element['data']['id'] != removed_node]
            layout['timestamp'] = time.time()
        return elements, layout

    app.run_server(debug=True)
