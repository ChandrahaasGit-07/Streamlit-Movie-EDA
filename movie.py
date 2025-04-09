import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page Title
st.set_page_config(page_title="EDA APP")
st.title('Interactive Data Explorer')

hide_st_style = '''
<style>
footer {visibility:hidden;}

/* Hide the GitHub logo (when the app is connected to GitHub) */
footer a[href="https://github.com/streamlit/streamlit"] {display: none;}

/* Hide the default app logo (Streamlit's default logo in the sidebar or header) */
header .css-1r8f6v1 {display: none;}

/* Optionally, you can add your custom logo instead of the Streamlit one */
.header .css-1y7jfhz {display: none;}  /* This hides the default Streamlit logo in the header */

fork {visibility:hidden;}
</style>
'''
st.markdown(hide_st_style,unsafe_allow_html=True)


# App dedscription- Expalin functionaliteis of the expander box
with st.expander('About the APP'):
    st.markdown('**What can this app do**.')
    st.info('This app shows the use of Pandas libaray for drawing the data wrangling, Altair for chart creating and editable dataframe for data interaction.') 
    st.markdown('**How to use this app?**')
    st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')

    # Question header
    st.subheader('Which movie best perform the ($) best at the box office?')
    
    # load the dataset
    df = pd.read_csv('movies_genres_summary.csv')
    df.year = df.year.astype('int')

    # Geners selection- Create a drodown menu for genre selection
    geners_list = df.genre.unique()
    geners_selection = st.multiselect('Select Geners', geners_list, ['Action','Adventure','Biography','Comedy','Drama','Horror'])

    # Year selection - Create a sidebar for year range selection
    year_list = df.year.unique()
    year_seletion = st.slider('Select the duration',1986,2006,(2000,2016))
    year_selection_list = list(np.arange(year_seletion[0], year_seletion[1]))

    # Subset data - Filter DataFrame based on selections
    df_selection = df[df.genre.isin(geners_selection) & df['year'].isin(year_selection_list)]
    reshaped_df = df_selection.pivot_table(index='year',columns='genre',values='gross',aggfunc='sum', fill_value=0)
    reshaped_df = reshaped_df.sort_values(by='year', ascending=False)

    # Editable dataFrame : Allow users to make live edits to the DataFrame
    df_editor = st.data_editor(reshaped_df, height=212, use_container_width = True,
                   column_config={'year': st.column_config.TextColumn('Year')},
                   num_rows = 'dynamic')
    
    # Data preparation - Prepare data for charting
    df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

    # Display line chart
    chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('gross:Q', title='Gross earnings ($)'),
            color='genre:N'
            ).properties(height=320)
    st.altair_chart(chart, use_container_width=True)
