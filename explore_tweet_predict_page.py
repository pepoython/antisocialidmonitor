import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

@st.cache #agar datanya bisa load secara real time
def load_data():
    df = pd.read_excel("tweet.xlsx", sheet_name='tweet')

    return df

def show_explore_page(df):
    st.title("Explore Tweet Prediction with Previous Model Classification")

    st.write(
        """
    ### Montioring Report of Tweet in Antisocialina
    """
    )

    data = df["classname_eng"].value_counts()

    st.write(
        """
    #### Time Series Tweet of Antisocialina
    """
    )

    df_classname = df.groupby([df['created_at'].dt.date, df['classname_eng']])['classname_eng'].count().reset_index(
        name="jumlah")
    series = pd.DataFrame({
        'created_at': df_classname.created_at,
        'classname_eng': df_classname.classname_eng,
        'count': df_classname.jumlah
    })

    # Basic Altair line chart where it picks automatically the colors for the lines
    basic_chart = alt.Chart(series).mark_line().encode(
        x='created_at',
        y='count',
        color='classname_eng',
        # legend=alt.Legend(title='Animals by year')
    )

    # Custom Altair line chart where you set color and specify dimensions
    custom_chart = alt.Chart(series).mark_line().encode(
        x='created_at',
        y='count',
        color=alt.Color('classname_eng',
                        scale=alt.Scale(
                            domain=['Non-Antisocial / General',
                                    'Failure to Conform to Social Norms Concerning Lawful Behaviour',
                                    'Irritability and Aggressiveness',
                                    'Reckless Disregard for Safety',
                                    'Lack of Remorse'],
                            range=['blue', 'red', 'green', 'orange', 'purple'])
                        )
    ).properties(
        width=900,
        height=500
    )

    # st.altair_chart(basic_chart)
    st.altair_chart(custom_chart)

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Percentage of Tweet in Antisocialina""")

    st.pyplot(fig1)


    st.write(
        """
    #### Tweet of Antisocialina
    """
    )

    data = df.classname.value_counts().sort_values(ascending=False)
    st.bar_chart(data)