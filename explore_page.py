import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'




@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df=df[df["Employment"].str.contains('Employed, full-time')]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df["Country"] != "Other"]

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2023
    """
    )

    data = df["Country"].value_counts()

    # Create a larger figure
    fig1, ax1 = plt.subplots(figsize=(10, 10))  # Adjust the figsize as needed

    # Explode a slice for emphasis
    explode = [0.1 if label == 'United States of America' else 0 for label in data.index]

    # Create the pie chart with improved settings
    wedges, texts, autotexts = ax1.pie(data, autopct="%1.1f%%", shadow=True, startangle=90,
                                       explode=explode)

    # Adjust labels for better readability
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(10)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis("equal")

    # Place the legend below the chart
    legend = ax1.legend(wedges, data.index, title="Countries", loc="upper center", bbox_to_anchor=(0.5, -0.15),
                        ncol=5)  # ncol for the number of columns

    # Adjust legend font size
    legend.get_title().set_fontsize('12')
    for text in legend.get_texts():
        text.set_fontsize('10')

    st.write("""#### Number of Data from Different Countries""")
    st.pyplot(fig1)

    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

