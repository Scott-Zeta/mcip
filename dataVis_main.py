import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode, DataReturnMode
import os

st.set_page_config(page_title="Code Analyzer",
                   page_icon=":shark:",
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items={
                       'Get Help': 'https://github.com/Scott-Zeta',
                       'Report a bug': "https://github.com/Scott-Zeta",
                       'About': "Made by a1795409 \n Scott Zeta"
                   })
st.write('<h1 style="color:#1AD0EA">Students Code Analysis</h1>',
         unsafe_allow_html=True,
         anchor=None)

with st.sidebar:
    file = st.file_uploader(label='',
                            type=['csv'],
                            accept_multiple_files=False)
    file_compare = st.file_uploader(label='This optional upload is for comparison',
                            type=['csv'],
                            accept_multiple_files=False)

overview, personal = st.columns([2, 1])
scmatrix, toplist = st.columns([2, 1])
pivot = st.container()

dataset_init = pd.DataFrame()
dataset_compare = pd.DataFrame()


def create_Radar(dataset, name):
    # df = pd.DataFrame(dict(
    # frequency = dataset[1:],
    # theta = ['functions','variables','conditionals','nestinglevels','assignments','branches','comparisons']))
    # fig = px.line_polar(df, r='frequency', theta='theta', line_close=True)
    # fig.update_traces(fill='toself')
    fig = go.Figure(data=go.Scatterpolar(
        r=dataset[1:],
        theta=[
            'functions', 'variables', 'conditionals', 'nestinglevels',
            'assignments', 'branches', 'comparisons'
        ],
        fill='toself',
        name=name))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True), ),
                      showlegend=False)
    return fig


def create_histogram(dataset, binsize):
    name = dataset.name
    fig = px.histogram(dataset, x=name, nbins=round(100 / binsize))
    return fig


def create_sc_matrix(dataset, list):
    if len(list) == 1:
        fig = px.scatter(dataset, x=list[0], hover_name="stud")
    elif len(list) == 2:
        fig = px.scatter(dataset, x=list[0], y=list[1], hover_name="stud")
    elif len(list) > 2:
        fig = px.scatter_matrix(dataset,
                                dimensions=list,
                                title="Scatter matrix",
                                hover_name="stud")
        fig.update_traces(diagonal_visible=False)
    return fig

def create_compare_his(dataset1, dataset2):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=dataset1,name = 'initial indication',hoverinfo='y'))
    fig.add_trace(go.Histogram(x=dataset2,name = 'comparing indication',hoverinfo='y'))

    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    return fig

if file:
    dataset_init = pd.read_csv(file, comment='#')
    #st.dataframe(data=dataset_init, width=None, height=None)

if file_compare:
    dataset_compare = pd.read_csv(file_compare, comment='#')

with personal:
    if not dataset_init.empty:
        st.subheader('Personal indication', anchor=None)
        option = st.selectbox('Who would you like to check?', (dataset_init))
        plot_data = dataset_init.set_index('stud').loc[[option
                                                        ]].values.tolist()[0]
        fig = create_Radar(plot_data, option)
        st.plotly_chart(fig, use_container_width=True)
        profile_card = st.container()
        with profile_card:
            st.write('Name:', option)
            st.write('Total Lines:', str(plot_data[1]))
            root = r"C:\Users\61694\OneDrive\Desktop\MCIProject\\" + option
            #You can change this root path
            open_button = st.button('Open Source Code')
            if open_button:
                try:
                    for filename in os.listdir(root):
                        with open(os.path.join(root, filename), 'r')as f:
                            #print(f.name)
                            os.startfile(f.name)
                except:
                    st.error("Fail! Can not find the folder or sourcefile has already open!")

with overview:
    if not dataset_init.empty and not dataset_compare.empty:
        st.subheader('Overview', anchor=None)
        option = st.selectbox(
            'Which Overview would you like to check?',
            (dataset_init.set_index('stud').columns.tolist()))
        #binsize = st.slider('Please choose the binsize', 1, 10, 5)
        plot_data = dataset_init[option]
        plot_compare = dataset_compare[option]
        fig = create_compare_his(plot_data, plot_compare)
        st.plotly_chart(fig, use_container_width=True)
    elif not dataset_init.empty:
        st.subheader('Overview', anchor=None)
        option = st.selectbox(
            'Which Overview would you like to check?',
            (dataset_init.set_index('stud').columns.tolist()))
        binsize = st.slider('Please choose the binsize', 1, 10, 5)
        plot_data = dataset_init[option]
        fig = create_histogram(plot_data, binsize)
        st.plotly_chart(fig, use_container_width=True)
        st.write(option, 'mean:', str(round(dataset_init.mean()[option], 3)),
                 ', standard deviation:',
                 str(round(dataset_init.std()[option], 3)))

with scmatrix:
    if not dataset_init.empty:
        st.subheader('Scatter Matrix', anchor=None)
        options_list = st.multiselect(
            'Which indications would you like to choose?', [
                'lines', 'functions', 'variables', 'conditionals',
                'nestinglevels', 'assignments', 'branches', 'comparisons'
            ], ['lines', 'functions'])
        if len(options_list) >= 1:
            fig = create_sc_matrix(dataset_init, options_list)
            st.plotly_chart(fig, use_container_width=True)

with toplist:
    if not dataset_init.empty:
        st.subheader('Top List', anchor=None)
        option = st.select_slider(
            'Select a indication you would like to check',
            options=[
                'lines', 'functions', 'variables', 'conditionals',
                'nestinglevels', 'assignments', 'branches', 'comparisons'
            ])
        order = st.radio(
            "Select you want to check top or bottom 10 students",
            ('ascending', 'descending'))
        # asc_or_des = True
        if order == 'ascending':
            asc_or_des = True
        elif order == 'descending':
            asc_or_des = False   
        df_top = dataset_init.sort_values(option,ascending = asc_or_des).head(10)
        st.write(df_top)
        # if order == 'ascending':
        #     dataset_init.loc[(dataset_init[option] >
        #                       dataset_init.mean()[option] +
        #                       2.326 * dataset_init.std()[option])]
        # elif order == 'descending':
        #     dataset_init.loc[(dataset_init[option] <
        #                       dataset_init.mean()[option] -
        #                       2.326 * dataset_init.std()[option])]

with pivot:
    if not dataset_init.empty:
        st.subheader('Pivot', anchor=None)
        gb = GridOptionsBuilder.from_dataframe(dataset_init)
        gb.configure_default_column(enablePivot=True,
                                    enableValue=True,
                                    enableRowGroup=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()
        gridOptions = gb.build()

        response = AgGrid(
            dataset_init,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=False,
        )

        df_selected = pd.DataFrame(response["selected_rows"])

        if not df_selected.empty:
            title = st.text_input('Flie name', 'selected_stu')
            st.download_button(
                label="Download selected data as CSV",
                data=df_selected.to_csv().encode('utf-8'),
                file_name=title+'.csv',
                mime='text/csv',
            )
