from shiny import ui
from data import sc_samples, degs, libraries

app_ui = ui.page_fluid(
    ui.navset_card_tab(
        ui.nav_panel(
            "Similarity Analysis",
            ui.layout_columns(
                # Primeiro card - inputs na mesma linha
                ui.card(
                    ui.layout_columns(
                        ui.input_selectize(
                            "dataset_choice",
                            "Select Dataset:",
                            choices=list(sc_samples.keys()) if 'sc_samples' in globals() else [],
                            multiple=False,
                            width="100%"
                        ),
                        ui.input_action_button("run_analysis", "Run Analysis", width="100%"),
                        col_widths=[8, 4],
                        gap="15px"
                    ),
                    height="120px"
                ),
                # Card da tabela com botão de download
                ui.card(
                    ui.download_button("download_table", "Download Table", class_="btn-primary"),
                    ui.output_data_frame("results_table"),
                    height="500px",  # Reduzido um pouco
                    full_screen=True
                ),
                # Card do heatmap
                ui.card(
                    ui.output_plot("heatmap_plot", height="400px"),
                    height="500px",  # Reduzido um pouco
                    full_screen=True
                ),
                col_widths=[12, 6, 6]
            )
        ),
        ui.nav_panel(
    "Enrichment Analysis",
    ui.layout_columns(
        # Card de inputs
        ui.card(
            ui.layout_columns(
                ui.input_selectize(
                    "degs_choice",
                    "Select DEGs Dataset:",
                    choices=list(degs.keys()) if 'degs' in globals() else [],
                    multiple=False,
                    width="100%"
                ),
                ui.input_selectize(
                    "contrast_choice",
                    "Select Contrast:",
                    choices=[],  # Será atualizado pelo server
                    multiple=False,
                    width="100%"
                ),
                ui.input_selectize(
                    "library_choice",
                    "Select Libraries:",
                    choices=libraries,
                    width="100%"
                ),
                ui.input_action_button("run_enrichment", "Run Enrichment", width="100%"),
                col_widths=[3, 3, 4, 2],
                gap="15px"
            ),
            height="140px"
        ),
        # Card da tabela de resultados
        ui.card(
            ui.download_button("download_enrichment", "Download Results", class_="btn-primary"),
            ui.output_data_frame("enrichment_table"),
            height="500px",
            full_screen=True
        ),
        # Card do gráfico de barras
        ui.card(
            ui.output_plot("enrichment_plot", height="400px"),
            height="500px",
            full_screen=True
        ),
        col_widths=[12, 6, 6]
    )
)
))
    