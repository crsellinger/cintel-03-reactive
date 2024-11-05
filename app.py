import plotly.express as px
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly
import palmerpenguins
import seaborn

#Penguins data set
penguins_df = palmerpenguins.load_penguins()

#Page options, specifically title
ui.page_opts(title="Caleb Sellinger - Module 2: Palmer Penguins Data", fillable=True)

#column component
with ui.layout_columns():

    #DataGrid for penguins data, 
    @render.data_frame
    def plot1():
        selected_species = input.selected_species_list()
        if selected_species:
            filtered = penguins_df[penguins_df["species"].isin(selected_species)]
        return render.DataGrid(filtered)

    #DataTable of penguins data
    @render.data_frame
    def plot2():
        selected_species = input.selected_species_list()
        if selected_species:
            filtered = penguins_df[penguins_df["species"].isin(selected_species)]
        return render.DataTable(filtered)

#column component
with ui.layout_columns():

    @render.plot(alt="Seaborn histogram plot")
    def plot3():
        return seaborn.histplot(data=penguins_df,x="species",y="body_mass_g",bins=input.seaborn_bin_count())
    
    @render_plotly
    def plot4():
        return px.histogram(data_frame=penguins_df,x="flipper_length_mm",y="body_mass_g",nbins=input.selected_number_of_bins())

#Card component for scatter plot
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    #Scatter plot for penguins data
    @render_plotly
    def plot5():
        island = [input.selected_island()]
        filtered = penguins_df[penguins_df["island"].isin(island)]
        return px.scatter(filtered,x="flipper_length_mm",y="body_mass_g",color="species",title="Body Mass vs Flipper Length",labels={"body_mass_g":"Body Mass (g)","flipper_length_mm":"Flipper Length (mm)","species":"Species"})
    
#Side bar component
with ui.sidebar(open="open",bg="#99ccff",fillable=True):
    ui.input_dark_mode(mode="light")
    ui.h2("Sidebar")
    ui.input_checkbox_group("selected_species_list","Select Species (Plot 1 & 2)",choices=["Adelie","Gentoo","Chinstrap"],selected=["Adelie","Gentoo","Chinstrap"],inline=False)
    ui.input_selectize(id="selected_island",label="Select Penguins Island",choices=["Torgersen","Biscoe","Dream"],selected="Dream")
    ui.input_slider("seaborn_bin_count","Seaborn Slider (Plot 3)",0,150,50)
    ui.input_numeric(id="selected_number_of_bins",label="Select Number of Bins (Plot4)",value=10)
    ui.hr()
    ui.a("Link HERE",href="https://github.com/crsellinger/cintel-02-data",target="_blank")