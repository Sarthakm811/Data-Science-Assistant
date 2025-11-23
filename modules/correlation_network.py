"""Correlation Network Graph Module"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import networkx as nx

class CorrelationNetwork:
    def __init__(self, df, threshold=0.5):
        self.df = df
        self.threshold = threshold
    
    def create_network(self):
        """Create correlation network graph"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr().abs()
        
        # Create network graph
        G = nx.Graph()
        
        # Add nodes
        for col in corr_matrix.columns:
            G.add_node(col)
        
        # Add edges for correlations above threshold
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if corr_matrix.iloc[i, j] > self.threshold:
                    G.add_edge(
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        weight=corr_matrix.iloc[i, j]
                    )
        
        # Calculate positions using spring layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        edge_weights = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_weights.append(G[edge[0]][edge[1]]['weight'])
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_size.append(len(G[node]) * 10 + 20)
        
        # Create figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color='lightblue',
                line_width=2
            ),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f'Correlation Network (threshold > {self.threshold})',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )
        
        return fig, G
    
    def get_correlation_pairs(self):
        """Get top correlated pairs"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr().abs()
        
        pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                if corr_matrix.iloc[i, j] > self.threshold:
                    pairs.append({
                        'Variable 1': corr_matrix.columns[i],
                        'Variable 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
        
        return pd.DataFrame(pairs).sort_values('Correlation', ascending=False)
