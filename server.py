from shiny import Inputs, Outputs, Session, reactive, render, ui
import asyncio
import pandas as pd

from functions import (
    compare_centroids_distance_correlation_from_df,
    plot_correlation_heatmap,
    convert_to_long_format
)
from data import sc_samples


def server(input, output, session):
    
    # Reactive value para armazenar os dados processados
    processed_data = reactive.Value(None)
    
    @reactive.Effect
    @reactive.event(input.run_analysis)
    def _():
        if not input.dataset_choice():
            return None
        
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", detail="This may take a while...")
            
            # Simula etapas do processamento
            for i in range(1, 15):
                p.set(i, message="Processing...")
                reactive.flush()
                
            selected_data = sc_samples[input.dataset_choice()]['df_pca_harmony']
            centroid_df, best_match = compare_centroids_distance_correlation_from_df(selected_data)
            processed_data.set(centroid_df)

    @output
    @render.data_frame
    def results_table():
        data = processed_data()
        if data is not None:
            # Converte para formato longo
            long_data = convert_to_long_format(data)
            return render.DataTable(
                long_data.round(5),
                filters=True,
                width="100%",
                height="400px"
            )
        return None

    @output
    @render.plot
    def heatmap_plot():
        data = processed_data()
        if data is not None:
            return plot_correlation_heatmap(data)
        return None

    @session.download(
        filename=lambda: f"similarity_analysis_{input.dataset_choice() or 'data'}.csv"
    )
    def download_table():
        data = processed_data()
        if data is not None:
            long_data = convert_to_long_format(data)
            
            # Criar arquivo CSV em memória
            from io import StringIO
            csv_buffer = StringIO()
            long_data.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            
            yield csv_buffer.getvalue()