from shiny import Inputs, Outputs, Session, reactive, render, ui
import asyncio
import pandas as pd
from io import StringIO
from functions import (
    compare_centroids_distance_correlation_from_df,
    plot_correlation_heatmap,
    convert_to_long_format,
    run_enrichment_analysis,
    create_horizontal_barplot
)
from data import sc_samples, degs


def server(input, output, session):
    
    processed_data = reactive.Value(None)
    
    @reactive.Effect
    @reactive.event(input.run_analysis)
    def _():
        if not input.dataset_choice():
            return None
        
        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", detail="This may take a while...")
            
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

    @render.download(
        filename=lambda: f"similarity_analysis_{input.dataset_choice() or 'data'}.csv"
    )
    def download_table():
        data = processed_data()
        if data is not None:
            long_data = convert_to_long_format(data)
            csv_buffer = StringIO()
            long_data.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            
            yield csv_buffer.getvalue()
    enrichment_results = reactive.Value(None)

    @reactive.Effect
    @reactive.event(input.degs_choice)
    def _():
        if input.degs_choice() and input.degs_choice() in degs:
            contrasts = list(degs[input.degs_choice()].keys())
            ui.update_selectize(
                "contrast_choice",
                choices=contrasts
            )

    # Executar análise de enrichment
    @reactive.Effect
    @reactive.event(input.run_enrichment)
    def _():
        # Validar inputs
        if (not input.degs_choice() or 
            not input.contrast_choice() or 
            not input.library_choice()):
            return None
        
        with ui.Progress(min=1, max=10) as p:
            p.set(message="Running enrichment analysis...", detail="This may take a while...")
            
            for i in range(1, 10):
                p.set(i, message="Processing...")
                reactive.flush()
            
            # Obter a lista de genes
            gene_list = degs[input.degs_choice()][input.contrast_choice()]['gene']
            
            # Executar enrichment analysis
            results = run_enrichment_analysis(
                gene_list=gene_list,
                libraries=input.library_choice(),
                organism='human'
            )
            
            enrichment_results.set(results)

    # Tabela de resultados
    @output
    @render.data_frame
    def enrichment_table():
        data = enrichment_results()
        if data is not None:
            return render.DataTable(
                data.round(5),
                filters=True,
                width="100%",
                height="400px"
            )
        return None

    # Gráfico de barras
    @output
    @render.plot
    def enrichment_plot():
        data = enrichment_results()
        if data is not None:
            return create_horizontal_barplot(data)
        return None

    # Download dos resultados
    @render.download(
        filename=lambda: f"enrichment_analysis_{input.degs_choice()}_{input.contrast_choice()}.csv"
    )
    def download_enrichment():
        data = enrichment_results()
        if data is not None:
            csv_buffer = StringIO()
            data.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            yield csv_buffer.getvalue()