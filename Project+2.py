
# coding: utf-8
# Module 4 & 5 - Data Visualization and Interpretation
# In[1]:


import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

get_ipython().magic('matplotlib inline')


# Diamonds are analyzed for quality by the 4Cs: cut, carat, clarity and color.
# Cut: ranked as Fair, Good, Very Good, Premium and Ideal - most important quality 
# Carat - weight of the diamond when cut
# Color - Color of the diamond, with D being the best and J the worst 
# Clarity - How obvious inclusions are within the diamond:(in order from best to worst, FL = flawless, I3= level 3 inclusions) FL,IF, VVS1, VVS2, VS1, VS2, SI1, SI2, I1, I2, I3 
# Depth - depth % :The height of a diamond, measured from the culet to the table, divided by its average girdle diameter 
# Table - table%: The width of the diamond's table expressed as a percentage of its average diameter
# Price - the price of the diamond
# x - length mm 
# y - width mm 
# z - depth mm
# 
# Table(54-57%) and depth(61-62.5%) percentages are the main measurements that determine the quality of cut and are used to weed out poorly cut diamonds.
# 
# Source: https://beyond4cs.com/grading/depth-and-table-values/

# In[23]:



# read the csv dataset for diamonds

dsloc = 'downloads/diamonds.csv'


df = pd.read_csv(dsloc)
df.head()


# In[24]:


#rename the pound/hashtag(#) column so it doesn't cause further issues
df.rename(columns={'Unnamed: 0': 'Number'}, inplace =True)


# # CHECK TO SEE HOW MANY RECORDS ARE IN INITIAL DATASET

# In[25]:


df.count()


# In[26]:


#set INDEX
df.set_index('Number', inplace=True)
df.head()


# In[27]:


columns = ['carat', 'cut', 'color', 'clarity', 'depth_percent','table_percent','price', 'l_mm','w_mm','d_mm']

#change column names for readability
df.columns = columns
df.head()


# # CLEAN THE DATA

# In[28]:


dupe = df.duplicated() #creates list of True/False values
df[dupe] #shows rows where duplicated is True


# # DELETE 146 RECORDS OF DUPLICATED DATA
# 

# In[29]:


#drops duplicate rows -- Likely false positive, but removing for now.
df = df.drop_duplicates()


# In[30]:


df.count()


# # CHECK NA VALUES AND DELETE; RESULTS REFLECTED NO NA VALUES

# In[31]:



#drop rows with any missing data
df = df.dropna()


# In[32]:


df.count()


# # FIND THE MAX PRICE AND DISPLAY THE ROW

# ### Determine the Shapes of Diamonds 

# In[33]:


import numpy as np


# ### Diamond Shapes 
# Heart Shaped Diamond- Cut Guide,Table % - 53 - 63, Depth % - 58 - 62, L/W Ratio - .95 - 1.02
# 
# Round Shaped Diamond-  Cut Guide,Table % - 53 - 58,Depth % - 59 - 62.3,L/W Ratio - 1.00
# 
# Princess Shaped Diamond- Cut Guide,Table %  - 67 - 72,Depth % - 64 - 75,L/W Ratio -  1.05 - 1.08
# 
# Oval Shaped Diamond- Cut Guide, Table % - 53 - 63   , Depth % - 58 - 62   , L/W Ratio - 1.35 - 1.6
# 
# Marquise Shaped Diamond- Cut Guide, Table %- 53 - 63   , Depth %- 58 - 62  , L/W Ratio - 1.75-2.15
# 
# Pear Shaped Diamond- Cut Guide, Table %-53 - 63  , Depth %- 58 - 62  , L/W Ratio - 1.40 - 1.70
# 
# Emerald Shaped Diamond- Cut Guide, Table %-61 - 69  , Depth %- 61 - 67  , L/W Ratio - 1.35 - 1.60
# 
# Asscher Shaped Diamond- Cut Guide, Table %-61 - 69   , Depth %- 61 - 67, L/W Ratio - 1.03 - 1.08
# 
# Radiant Shaped Diamond- Cut Guide, Table % - 61 - 69  , Depth % - 61 - 67  , L/W Ratio - 1.15 - 1.35
# 
# Cited from: https://www.lumeradiamonds.com/diamond-education/
# 
# 

# In[34]:


# Calculated Length/Width Ratio to get a better picture of the diamond shape 
#f np.where(df['w_mm'] > 0):
df['LWRatio'] = np.divide(df['l_mm'], df['w_mm'])
df['design'] =           np.where(((df['LWRatio'] >= .95) & (df['LWRatio']<1.03)),'Round or Heart',
                                 np.where(((df['LWRatio'] >= 1.03) & (df['LWRatio'] < 1.05)), 'Asscher', 
                                          np.where(((df['LWRatio'] >= 1.05) & (df['LWRatio'] <= 1.08)),'Princess or Asscher',
                                                  np.where(((df['LWRatio'] > 1.08) & (df['LWRatio'] < 1.35)),'Radiant',
                                                          np.where(((df['LWRatio'] >= 1.35) & (df['LWRatio'] < 1.40)),'Emerald or Oval',
                                                                  np.where(((df['LWRatio'] >= 1.40) & (df['LWRatio'] <= 1.60)),'Emerald, Pear or Oval',
                                                                           np.where(((df['LWRatio'] > 1.60) & (df['LWRatio'] <= 1.70)),'Pear',
                                                                                   np.where((df['LWRatio'] > 1.70),'Marquise','Zero Divisor - N/A'))))))))
df.head()


# ### COUNT THE DIAMONDS BY SHAPE

# In[35]:




df = df.drop(df[df['design'] != 'Round or Heart'].index)

df 




# In[36]:


df.groupby('design').count()


# In[41]:


df.groupby(['color','cut']).std()


# # PLOT THE DATA 

# ## This shows a plot graph with Table (face of the diamond) vs Price of diamonds.
# ## Conclusion with this plot graphic is the majority of the Tables (face size of the diamond) lie between 50mm and 70mm ranging in price from 326 dollars to 18,823 dollars.

# In[45]:


interests = {'color','cut','clarity'}


# In[56]:


for interest in interests :
    sns.lmplot(x='carat', y='price', hue=interest,data=df)
    sns.violinplot(x=interest,y='price',data=df)


# In[57]:


import statsmodels.formula.api as smf


# In[65]:


interests


# In[72]:


result = smf.ols('price ~ color + cut + clarity ', data=df).fit()


# In[62]:


result.summary()


# In[86]:


df


# In[87]:


import statsmodels.formula.api as smf






# In[89]:


smresults = smf.ols('price ~ carat + cut + clarity', df).fit()



# In[90]:



df['pred'] = smresults.predict()


# In[104]:


smresults.predict(pd.df({'price': df(df['price'])
                          }))


# In[82]:


array1 = result.predict()
array1.count()

print(array1)
# ### SCATTER PLOT SHOWING THE RELATIONSHIP OF PRICE AND CARAT WITH CLARITY OF DIAMONDS.
# ### THIS SHOWS A STRONG POSITIVE RELATIONSHIP 

# In[ ]:


g = sns.lmplot(x='carat', y='price', hue='clarity', x_bins=50, height=10,aspect=2, data=df)


# ### Visualize all Types by Stat

# In[ ]:


#create a column that contains all stat types and a column for their corresponding value
melt_df = pd.melt(df, 
                  id_vars=['clarity', 'cut', 'color'], #column to keep
                  var_name="Stat")

melt_df.head()


# In[ ]:


#melted datframe has 6 times the amount of rows as original stats dataframe
#6 rows for each pokemon for each stat type
print(df.shape)
print(melt_df.shape)


# In[ ]:


#create a histogram 
sns.distplot(df['carat'])


# In[ ]:


sns.distplot(df['price'])


# ### SUMMARY CONCLUSION ABOUT THE DIAMOND CSV DATA
#  Initially 53,940 records.
#  146 records were duplicates and removed resulting in 53,794 records to analyze.
#  The diamonds range in price from 346 to 18,823 dollars.
#  The carat size ranges from .2 cts to 5.01 cts. 
#  There is a positive relationship between Price and Carat.
#  The majority of the diamonds are Ideal cuts, G in color, and SI1 clarity.  
#  The average size of diamond is ~ .80 cts. and average price of 3933 dollars however it is not a true representation of the diamond data. The histograms of price and carat reflect the diamond data is not a Normal Distribution but a Poisson Distribution which means the data is heavily represented in one area more than the rest of the data. Using the median data would be a more acurate representation of the data so therefore the Median size of diamond is ~ .70 cts and median price is 2401 dollars.
#  
#  The majority of the diamonds appear to be Heart Shaped.
