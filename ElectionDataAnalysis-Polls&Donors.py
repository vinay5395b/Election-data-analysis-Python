# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 15:03:48 2019

@author: Vinay
"""
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from __future__ import division


#for vis
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

#for fetching and reading data
import pandas_datareader.data as wb
from datetime import datetime as dt

# Use to grab data from the web(HTTP capabilities)
import requests

#to work with the csv file, the DataFrame will require a .read() method
from StringIO import StringIO  

url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"

source = requests.get(url).text  #to get info in text form
poll_data = StringIO(source)  # Use StringIO to avoid an IO error with pandas

poll_df = pd.read_csv(poll_data)
poll_df.to_csv('Election Data.csv')
#Convert date from string to Timestamp
from datetime import datetime

poll_df['End Date1'] = poll_df['End Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
poll_df['Start Date1'] = poll_df['Start Date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
#poll_df=pd.read_csv('Election Data.csv')
poll_df.info()
poll_df.head()

poll_df.drop('Question Text',axis=1,inplace=True)
poll_df.drop('Other',axis=1,inplace=True)
poll_df.drop('Question Iteration',axis=1,inplace=True)


poll_df=poll_df.drop(columns=['Other'])
poll_df.info()

sns.countplot('Affiliation',data=poll_df)
sns.countplot('Affiliation',data=poll_df,hue='Population')
poll_df.head()

#averages of votes

avg=pd.DataFrame(poll_df.mean())
avg.drop('Number of Observations',axis=0,inplace=True)
avg.head()

std=DataFrame(poll_df.std())
std.drop('Number of Observations',axis=0,inplace=True)
std.head()

avg.plot(yerr=std,kind='bar',legend=False)

poll_avg= pd.concat([avg,std],axis=1)
poll_avg.columns=['Average','STD']


#Q.3).) How do undecided voters effect the poll?

poll_df.plot(x='End Date1',y=['Obama','Romney','Undecided'],linestyle='',figsize=(15,5),marker='o')

#Q.5)How did voter sentiment change over time?
poll_df['Difference']=(poll_df.Obama-poll_df.Romney)/100 #converting their vote difference to percentage
poll_df.head()

poll_df=poll_df.groupby(['Start Date'],as_index=False).mean()
poll_df.head()
poll_df.plot(x='Start Date1',y='Difference',figsize=(12,4),marker='o',linestyle='-')

row_in=0
xlimit=[]

for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in+=1
    else:
        row_in+=1

print min(xlimit)
print max(xlimit)

poll_df.plot(x='Start Date',y='Difference',figsize=(12,4),marker='o',linestyle='-',xlim=(325,352))

# Analysis and sentiment change after the debates which were in the month of october '12
#Oct 3rd
plt.axvline(x=325+2,linewidth=4,color='grey')

#Oct 11th
plt.axvline(x=325+10,linewidth=4,color='grey')

#Oct 22nd
plt.axvline(x=325+21,linewidth=4,color='grey')


#PART II
###For donors dataset #########

donor_df= pd.read_csv('C:\Users\ADMIN\.spyder\Election_Donor_Data.csv')
donor_df.info()

donor_df.head()

donor_df['contb_receipt_amt'].value_counts()     #to get frequency of each unique value in that column

don_mean=donor_df['contb_receipt_amt'].mean()
don_std=donor_df['contb_receipt_amt'].std()
print 'The average donation was %.2f with a std of %.2f'%(don_mean,don_std)

top_donor = donor_df['contb_receipt_amt'].copy()
top_donor.sort_values()

#get rid of the -ve values
top_donor=top_donor[top_donor>0]
top_donor.sort_values()

top_donor.value_counts().head()

com_don = top_donor[top_donor<=2500]
com_don.hist(bins=100)

candidates=donor_df.cand_nm.unique()    #getting names of candidates
candidates

#Mapping the names of the candidates to their parties

# Dictionary of party affiliation
party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

# Now map the party with candidate
donor_df['Party'] = donor_df.cand_nm.map(party_map)

#Q.) How did the donations differ between candidates?
donor_df = donor_df[donor_df.contb_receipt_amt>0]
donor_df.head()
donor_df.groupby('cand_nm')['contb_receipt_amt'].count()

donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()
cand_amount= donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

i=0

for don in cand_amount:
    print "The candidate %s raised %.0f dollars \n" %(cand_amount.index[i],don)
    i+=1

#Q.) How did the donations differ between Democrats and Republicans?
cand_amount.plot(kind='bar')

donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')

#Q.) What were the demographics of the donors?

occupation_df = donor_df.pivot_table('contb_receipt_amt',index='contbr_occupation',columns='Party',aggfunc='sum')

occupation_df.head()
occupation_df.tail()

occupation_df.shape

occupation_df= occupation_df[occupation_df.sum(1)>1000000]
occupation_df.shape
occupation_df.plot(kind='bar')

occupation_df.plot(kind='barh',figsize=(10,12)) #plotting horizontal bar graph

# Drop the unavailble occupations
occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)

######IMP(combining 2 columns to make 1)####
#Combine CEO and C.E.O to make a single column
occupation_df.loc['CEO']= occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']
occupation_df.drop('C.E.O.',inplace=True)

occupation_df.plot(kind='barh',figsize=(10,12)) #plotting horizontal bar graph
