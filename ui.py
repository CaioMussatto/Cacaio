from shiny import ui
from data import sc_samples

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
        )
    )
)


