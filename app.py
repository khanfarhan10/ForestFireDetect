import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import folium
import ee
import geemap
import os

Map = geemap.Map()

# Load the Nighttime Image Collection
RTMA_Image_Collection = 'NOAA/NWS/RTMA'
all_collection = ee.ImageCollection(RTMA_Image_Collection)

from datetime import datetime, timedelta
date_today = datetime.today().strftime('%Y-%m-%d')
date_yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

print("Date Today :",date_today,"| Date Yesterday :",date_yesterday)

dataset = all_collection.filter(ee.Filter.date(date_yesterday, date_today))

Map.add_basemap('Google Satellite') # 'Google Satellite' / Terrain

# Draw any shapes on the map using the Drawing tools before executing this code block
try :
    feature = Map.draw_last_feature
except:
    feature=None
if feature is None:

    geom = ee.Geometry.Polygon([[[-124.86316,56.97715],
    [-70.20644,53.78275],
    [-73.90380, 26.83366],
    [-134.74959, 27.33460]]])
    feature = ee.Feature(geom, {})

roi = feature.geometry()
from copy import deepcopy
aoi = deepcopy(roi)

feat = ee.Feature(roi)
Map.addLayer(feat);
Map.centerObject(feature,4);

# sf = ee.Geometry.Point([-122.47555371521855, 37.76884708376152]);
# Amazon Rainforests
P1 = (-3.03014,-62.60020)
P2 = (-3.71241,-61.74739)

# North America
P1 = (-40,-20)
P2= (40,20)

# South America
P1 = (7.3625,266.9549)
P2= (-52.9089,335.1825)

x1,y1 = P1
x2,y2 = P2

# roi = ee.Geometry.Rectangle([-40, -20, 40, 20])
roi = ee.Geometry.Rectangle([x1,y1,x2,y2])
bounded = dataset.filterBounds(roi)

def getMidpoint(P1,P2):
  x1,y1 = P1
  x2,y2 = P2

  xCenter = (x1 + x2) / 2
  yCenter = (y1 + y2) / 2

  return xCenter,yCenter

PCenter = getMidpoint(P1,P2)

xCenter,yCenter = PCenter

# Extract the first image
first_image = bounded.first()
 
# Display band information about the image
first_image.bandNames().getInfo()

lengthCollection = bounded.size()
listOfImages = ee.Image(bounded.toList(bounded.size()));
firstImage = ee.Image(listOfImages.get(0));
secondImage = ee.Image(listOfImages.get(1));
lastImage = ee.Image(listOfImages.get(lengthCollection.subtract(1)));

# Compute the median in each band, each pixel.
# Band names are B1_median, B2_median, etc.
median = bounded.reduce(ee.Reducer.median());
median.bandNames().getInfo()

# The output is an Image.  Add it to the map.
vis_param = {"bands": ['TMP_median', 'WDIR_median', 'WIND_median'], "gamma": 0.8};

# Map.setCenter(-122.3355, 37.7924, 9);

Map.addLayer(median, vis_param, RTMA_Image_Collection, True, 1)




# df = pd.read_csv("forestfires.csv")
#all functions
# @st.cache
def welcome():
    return "Welcome All"
# @st.cache    
def predict_forest_fire(x,y,month,ffmc,dmc,dc,temp):
    prediction = model.predict([[x,y,month,ffmc,dmc,dc,temp]])
    print(prediction)
    return prediction

# @st.cache
def main_prediction():
    # st.title("Forest Fire Prediction")
    # st.markdown("""<center><img src='https://upload.wikimedia.org/wikipedia/commons/d/d8/Deerfire_high_res_edit.jpg' width='500px'></center>""",unsafe_allow_html=True)
    # st.markdown("""<br>""",unsafe_allow_html=True)
    
    html_temp = """
    <div style="background-color:#00b3ff;padding:10px">
    <h2 style="color:white;text-align:center;">Forest Fire Prediction</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    img_top = """<center><img src="https://i.imgur.com/yOS7IGv.png" width="700px"></center>"""
    st.markdown(img_top,unsafe_allow_html=True)
    st.markdown("""<br>""",unsafe_allow_html=True)
    with st.echo():
        folium_static(Map)
        
# @st.cache
def corr_plot():
    # st.write("You selected",len(location),"locations")
    
    # st.text("see plots")
    # df = pd.read_csv("forestfires.csv")
    # st.dataframe(df)
    
    corr = df.corr()

    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(5, 5))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title('Correlation Plot',size=15)

    st.pyplot(f)

@st.cache(suppress_st_warning=True)
def pair_plot():
    # df = pd.read_csv("forestfires.csv")

    # fig = plt.figure(figsize=(3,4))
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # fig = plt.figure()
    # sns.set_style('whitegrid')
    sns.pairplot(df)
    plt.title("Pair Plot")
    # plt.show()
    st.pyplot()


def V_corr_plot():
    # df = pd.read_csv("forestfires.csv")
    corr_new_train=df.corr()
    fig = plt.figure(figsize=(3,4))
    sns.heatmap(corr_new_train[['area']].sort_values(by=['area'],ascending=False).head(60),vmin=-1, cmap='seismic', annot=True)
    plt.title("Vertical Correlation plot")
    st.pyplot(fig)   

def threeD_Plot():
    # df = pd.read_csv("forestfires.csv")
    dmc = list(df['DMC'])
    temp = list(df['temp'])
    area = list(df['area'])
    train_f1 = pd.DataFrame(dmc,columns=['Dmc'])
    train_f2 = pd.DataFrame(temp,columns=['Temp'])
    train_target = pd.DataFrame(area,columns=['Target'])
    train_data = pd.concat([train_f1,train_f2,train_target],axis = 1)
    # train_data.head(5)
    sns.set_style("whitegrid", {'axes.grid' : False})

    fig = plt.figure(figsize=(3,3))

    ax = Axes3D(fig) # Method 1
    # ax = fig.add_subplot(111, projection='3d') # Method 2

    x = np.random.uniform(1,20,size=20)
    y = np.random.uniform(1,100,size=20)
    z = np.random.uniform(1,100,size=20)


    ax.scatter(train_data['Dmc'], train_data['Temp'], train_data['Target'], c=train_data['Dmc'],marker='o')
    ax.set_xlabel('Dmc')
    ax.set_ylabel('Temp')
    ax.set_zlabel('Target')
    ax.set_title("3D Scatter plot of DMC,temp and area")

    # plt.show()
    st.pyplot(fig)

def get_pie_plot(feature):
  df['area'] = df['area'].apply(lambda x : np.log(x+1))
  df1 = df.groupby(feature).sum()  
  df1 = df1[df1.area >0 ]

  theme = plt.get_cmap('hsv')
  cs = theme(np.arange(len(df1.area))/len(df1.area))
  fig, ax = plt.subplots(figsize = (3, 3))
  plt.pie(df1.area,labels = df1.index, colors = cs)
  plt.title("Relative amount of area affected per "+feature, fontsize = 14)
  # plt.show()
  st.pyplot(fig)

def load_img(img_name):
    img = Image.open(img_name)
    st.image(img,width=800)

#sidebar Edit
# st.title("hello")
html_img = """<center><img src="https://i.ibb.co/VY5wCkN/47480912-png.png" width="130px"></center>"""
st.sidebar.markdown(html_img,unsafe_allow_html=True)

st.sidebar.markdown("""## Navigation Bar: <br> """,unsafe_allow_html=True)
st.markdown("""<br><br>""",unsafe_allow_html=True)
red = st.sidebar.radio(" ",["Prediction","About the Project","Collaborators of the Project"])
# st.markdown("""<br></br> <br>""",unsafe_allow_html=True)
st.sidebar.markdown("""<br><br><br><br><br> Thank you for visiting the site🤗""",unsafe_allow_html=True)
st.sidebar.markdown(""" [  Our Github Repository](https://github.com/khanfarhan10/ForestFireDetect)""",unsafe_allow_html=True)



if red=="Prediction":
    main_prediction()
            
            
            
        
if red == "About the Project":
    # st.text("hello world")
    components.html(
    """
    <div style="background-color:#ff0055;padding:10px">
    <h2 style="color:white;text-align:center;">About the Project</h2>
    </div>   
    """
    )
    img_top = """<center><img src="https://i.imgur.com/yOS7IGv.png" width="700px"></center>"""
    st.markdown(img_top,unsafe_allow_html=True)
    topic= """
    
    <br>
    
    The main motive of this project is to predict the amount of area that can get 
    burned in a forest fire based on some parameters like `Humidity(RH)`, `Wind(wind)`,`Rain(rain)`, 
    `Temperature(temp)` etc. 
    
    This project is focused on a technical solution towards sustainability. Forestfire is one of the major concerns as it is getting worse day by day. 
    The problem with forest fires is their uncontrolled spreading nature and their sheer sudden eruptability.
    Most forest fire control departments are informed of fires when it's already too late. For this we introduce an UI where the user will give user credentials 
    with the latitude & longitude of the target area. We are sending these data in the form of API with SQL queries to Cloud. 
    With the help of IBM Cloud these information will be stored safely. We have also created a ML model which is capable of doing instance segmentation. 
    This model will segregate fire in three parts on the basis of intensity of the fire (eg.- HIGH, MODERATE, LOW). Also an alarm will be there to alert in urgency. 
    
    <p style="color:blue;">If you liked this project then it will be really motivating for us if you can star our <a href="https://github.com/khanfarhan10/ForestFireDetect">Github Repository</a>😄.</p>
     

    """
    
    ignore = """
        
    <br>
    
    [![ReadMe Card](https://github-readme-stats.vercel.app/api/pin/?username=khanfarhan10&repo=ForestFireDetect&theme=dark)](https://github.com/khanfarhan10/ForestFireDetect)

    """
    
    st.markdown(topic,unsafe_allow_html=True)
    
    
    
    
if red=="Collaborators of the Project":
    
    # html_colab = """
    # <div style="background-color:#29ffea;padding:10px">
    # <h2 style="color:white;text-align:center;">Collaborators:</h2>
    # </div><br>
    # """
    # st.markdown(html_colab,unsafe_allow_html=True)
    # img_top = """<center><img src=" https://github.com/debangeedas.png?sixe=40" width="700px"></center>"""
    # st.markdown(img_top,unsafe_allow_html=True)
    # st.markdown("""<br>""",unsafe_allow_html=True)
    
    components.html(
    """
    <div style="background-color:#ffe100;padding:10px">
    <h1 style="color:white;text-align:center;">Collaborators:</h1>
    </div>
    <br>
    <br>
    """
    )
    
    components.html(
    
    """
    <html>
        <head>
            
        </head>

        <body>
            <a>
                <strong style="font-size:20px">
                    <!-- khanfarhan10 &nbsp;&nbsp;-->
                    <pre class="tab">khanfarhan10 <a style="font-size:14px">26 commits </a><a style="color: #2bff00;font-size:10px">18,069++ </a><a style="color: #FF0000;font-size:10px">9,501--</a>   soumya997 <a style="font-size:14px">3 commits </a><a style="color: #2bff00;font-size:10px">19,938++ </a><a style="color: #FF0000;font-size:10px">3,460--</a></pre>
                    <div class="github-card" data-github="khanfarhan10" data-width="350" data-height="150" data-theme="default"></div>
                    <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                    <div class="github-card" data-github="soumya997" data-width="350" data-height="" data-theme="default"></div>
                    <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                </strong> 
                <br>
                <strong style="font-size:20px">
                    <!-- 1khanfarhan10 &nbsp;&nbsp;-->
                    <pre class="tab">Nibba2018 <a style="font-size:14px">2 commits </a><a style="color: #2bff00;font-size:10px">25++ </a><a style="color: #FF0000;font-size:10px">27--</a>           Dsantra92 <a style="font-size:14px">1 commits  </a><a style="color: #2bff00;font-size:10px">1,129++ </a><a style="color: #FF0000;font-size:10px">0--</a></pre>
                    <div class="github-card" data-github="Nibba2018" data-width="350" data-height="" data-theme="default"></div>
                    <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                    <div class="github-card" data-github="Dsantra92" data-width="350" data-height="" data-theme="default"></div>
                    <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                </strong>
                <br> 
                <strong style="font-size:20px">
                    <!-- 1khanfarhan10 &nbsp;&nbsp;-->
                    <pre class="tab">debangeedas <a style="font-size:14px">1 commits </a><a style="color: #2bff00;font-size:10px">40++ </a><a style="color: #FF0000;font-size:10px">0--</a>          BALaka-18 <a style="font-size:14px">1 commits </a><a style="color: #2bff00;font-size:10px">5++ </a><a style="color: #FF0000;font-size:10px">4--</a></pre>
                    <div class="github-card" data-github="debangeedas" data-width="350" data-height="" data-theme="default"></div>
                    <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                    <div class="github-card" data-github="BALaka-18" data-width="350" data-height="" data-theme="default"></div>
            <script src="//cdn.jsdelivr.net/github-cards/latest/widget.js"></script>
                </strong> 
                
        </body>
    </html>


    


        """,
        height=700,scrolling=True,width=800
    )
    
    
        
        

        
        
   


