from shiny import ui
from data import sc_samples, degs, libraries

app_ui = ui.page_fluid(
    ui.tags.style("""
        .btn-custom-height {
            height: 100px !important;
            padding-top: 8px !important;
            padding-bottom: 8px !important;
        }
    """),
    ui.navset_card_tab(
        ui.nav_panel(
            "Similarity Analysis",
            ui.layout_columns(
                ui.card(
                    ui.input_selectize(
                        "dataset_choice",
                        "Select Dataset:",
                        choices=list(sc_samples.keys()),
                        multiple=False
                    ),
                ),
                ui.input_action_button("run_analysis", "Run Analysis", width="100%", class_="btn-custom-height"),
                ui.card(
                    ui.download_button("download_table", "Download Table", class_="btn-primary"),
                    ui.output_data_frame("results_table"),
                    full_screen=True
                ),
                ui.card(
                    ui.output_plot("heatmap_plot", height="400px"),
                    full_screen=True
                ),
                col_widths=[8, 2, 6, 6]
            )
        ),
        ui.nav_panel(
            "Enrichment Analysis",
            ui.layout_columns(
                ui.card(
                    ui.layout_columns(
                        ui.input_selectize(
                            "degs_choice",
                            "DEGs Dataset:",
                            choices=list(degs.keys()),
                            multiple=False
                        ),
                        ui.input_selectize(
                            "contrast_choice", 
                            "Contrast:",
                            choices=[],
                            multiple=False
                        ),
                        ui.input_selectize(
                            "library_choice",
                            "Libraries:",
                            choices=libraries,
                            multiple=False
                        ),
                        col_widths=[4, 4, 4],
                        gap="10px"
                    ),
                ),
                ui.input_action_button("run_enrichment", "Run Enrichment", width="100%", class_="btn-custom-height"),
                ui.card(
                    ui.download_button("download_enrichment", "Download Results", class_="btn-primary"),
                    ui.output_data_frame("enrichment_table"),
                    full_screen=True
                ),
                ui.card(
                    ui.output_plot("enrichment_plot", height="400px"),
                    full_screen=True
                ),
                col_widths=[9, 2, 6, 6]
            )
        ),
        ui.nav_panel(
            "Cross-Modal Integration", 
            ui.layout_columns(
                ui.card(
                    ui.input_selectize(
                        "cross_modal_cancer",
                        "Cancer Dataset:",
                        choices=list(sc_samples.keys()),
                        multiple=False
                    ),
                ),
                ui.card(
                    ui.input_file(
                        "bulk_upload",
                        "Upload Bulk Data:",
                        accept=[".csv"]
                    )),
                ui.input_action_button("run_cross_modal", "Run Integration", width="100%", class_="btn-custom-height"),
                ui.card(
                    ui.download_button("download_cross_modal", "Download Matrix", class_="btn-primary"),
                    ui.output_data_frame("cross_modal_table"),
                    full_screen=True
                ),
                ui.card(
                    ui.output_plot("cross_modal_plot", height="400px"),
                    full_screen=True
                ),
                col_widths=[4, 4, 2, 6, 6]
            )
        )
    )
)