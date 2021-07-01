"""
Name:   Nidhish Yarlagadda
CS230:  Section 2F
Data:   Volcanoes.csv
URL:    https://share.streamlit.io/gibbsv3/project/main/volcano.py

Description: This program puts the volcanoes.csv file in a dataframe and runs several queries. It plots all the volcanoes
on a map and it calculates the top 10 countries with the most volcanoes and displays the results in a bar chart. It also
creates a random integer and uses it to display data for a random type of volcano. It shows a map of the volcanoes and
calculates and displays how many volcanoes there are of a certain rock type. It displays this information in a bar chart
of all the rock types of a particular volcano type.
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import random as rd

def mostVolcanoes(df): # graphs barchart of top 10 countries with the most Volcanoes
    df2 =(df[['Volcano Number','Country']].groupby('Country').count()) # creates new df with countries as indexes
    df2 = df2.sort_values(by='Volcano Number',ascending=False) # sorts it in descending order

    fig,ax = plt.subplots()
    ax.yaxis.grid(linestyle='dashed',zorder=0) # grid
    ax.bar(df2.index[0:10],df2['Volcano Number'][0:10],color = 'darkred',zorder=5) # bars. df is filtered for only the first 10 values

    ax.set_title("Countries with most Volcanoes")
    ax.set_xlabel("Countries")
    ax.set_ylabel("Number of Volcanoes")
    plt.xticks(rotation=-45)

    ax.set_facecolor('lightgrey')
    fig.patch.set_facecolor('lightgrey')

    st.header("Countries with the most Volcanoes")
    st.write(fig)
    st.write("As you can see, the United States has a lot of volcanoes!")

def volcanoesType(df , type): # outputs data for a specific type of volcano
    df2 = df[df['Primary Volcano Type'] == type]

    st.header(f"You are viewing information for **{type}** volcanoes!")
    st.subheader("Here is a map to visualize where these volcano(es) are located!")

    map(df2)
    st.write("The following graph describes how many volcano(es) of each rock type there are for this volcano type.")
    rocks(df2)
    st.write("Here are all the volcanoes in case you want to visit their websites: ")
    st.write(df2[['Volcano Name','Link']])
def rocks(df): # outputs graph visualizing how many volcanoes there or of a rock type

    df2 = df[['Dominant Rock Type', 'Volcano Number']].groupby('Dominant Rock Type').count() # new df with just rock type and count
    df2 = df2.sort_values(by='Volcano Number',ascending=False)

    fig,ax = plt.subplots()
    ax.xaxis.grid(linestyle='dashed',zorder=0)
    ax.barh(df2.index,df2['Volcano Number'],color = 'tab:brown',zorder=5) # creates horizontal bar graph
    ax.set_title("Volcanoes By Dominant Rock Type")
    ax.set_ylabel("Rock Type")
    ax.set_xlabel("Number of Volcanoes")

    # formatting
    ax.set_facecolor('lightgrey')
    fig.patch.set_facecolor('lightgrey')
    st.write(fig)

def unique(df , column): # this creates a dictionary of unique values in a column

    df2 = df[[column,'Volcano Number']].groupby(column).count() # dataframe with only type of volcano and count
    values = [index for index in df2.index] # creates list of only types of volcanoes
    counter = 1

    values_dict = {}
    for value in values: # creates dictionary for types of volcanoes
        values_dict[counter] = value
        counter += 1

    return values_dict

def map(df): # creates a map of all the volcanoes in a df
    df2 = df
    df2 = pd.DataFrame(df[['Volcano Name','Latitude','Longitude']],columns= ['Volcano Name','lat','lon'])

    df2['lat'] = df['Latitude'] # needed to create new dfs because columns were messed up in origianal df
    df2['lon'] = df["Longitude"]
    st.map(df2)

def greeting(name = "anonymous"): # welcome page
    st.header(f"Hello **{name}** and welcome to Nidhish Yarlagadda's Volcanoes Page!")
    # writes gifs
    st.markdown("![Alt Text](https://media.giphy.com/media/5zjJfdoitd4Ck/giphy.gif)")
    st.markdown("![Alt Text](https://media.giphy.com/media/BmISCc5IfXPt2686im/giphy.gif)")
    st.write("Use the navigation pane on the **sidebar** to view interesting information about volcanoes!")

def main():
    FILE = "volcanoes.csv"
    df = pd.read_csv(FILE)
    DIVIDER = "-" * 20

    st.sidebar.header("Volcanoes")
    st.sidebar.subheader("by Nidhish Yarlagadda")
    st.sidebar.write(DIVIDER)
    # stores page names in a list
    page_names = ['Welcome' , 'Map of Volcanoes' , 'Top 10 Countries with the Most Volcanoes' , 'Info about a Random Type of Volcano']
    nav = st.sidebar.radio('Navigation',page_names) # used for navigation
    # navigation conditions
    if nav == 'Welcome':
        input = st.text_input("Please Enter Your Name... Or hit ENTER to remain anonymous", "")
        if input == "":
            greeting()
        else:
            greeting(input)

    elif nav =='Map of Volcanoes':
        st.header("Volcanoes Around the World")
        map(df)
        st.write("The visualization shows all the volcanoes in the world. As you can see, there are a lot of volcanoes in the US!")

    elif nav == 'Top 10 Countries with the Most Volcanoes':
        mostVolcanoes(df)

    elif nav == 'Info about a Random Type of Volcano':
        types_dict = unique(df,'Primary Volcano Type')
        number = rd.randint(1,len(types_dict)) # generates random number used to select type of volcano
        #print(number)
        #print(types_dict[number])
        volcanoesType(df, types_dict[number])

    st.sidebar.write(DIVIDER)


main()
