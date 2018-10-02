import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import sys
myCSV="US_crime_1960_2005.csv" #### <------ENTER DESIRED FILE HERE 

if (myCSV=="marriage_divorce.csv"):
	#read the original data
        df = pd.read_csv('data.csv')
        
        #stack the 'State' columns
        stacked_df = df.set_index(['State']).stack(dropna=False)
        
        #reset the index to reshape the data
        newdf = stacked_df.reset_index()
        
        #seperate year and rate type of the unstacked columns
        yrlist = newdf.level_1.str.split(' ')
        
        #create 'Year' column, put the first element (year) from the list
        newdf['Year'] = [i[0] for i in yrlist]
        
        #create 'Rate Type' column, put the second element (divorce/marriage) rom the list
        newdf['Rate Type'] = [i[1] for i in yrlist]
        
        #create '% value' column, put the values into the column
        newdf[' % value'] = newdf[0]
        
        #drop the 'level_1' column
        outputdf = newdf.drop(['level_1',0], axis = 1)
        
        #output the data to a csv file
        outputdf.to_csv('clean_marriage_divorce.csv', index=False)
if (myCSV=="US_crime_1960_2005.csv"):
	df = pd.read_csv('US_crime_1960_2005.csv')
	idvars_list = ['Region','Division','State']
	valvars_list = ['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
                    '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', 
                     '1977','1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', 
                     '1986','1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', 
                     '1995','1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', 
                     '2004','2005']
                     
	result_df = pd.melt(df,id_vars = idvars_list, value_vars = valvars_list, var_name = 'Year',
                            value_name = 'Total')
	print(result_df.head())
	result_df.to_csv('crime_cleaned.csv',index = False)
if (myCSV=="migration.csv"):
	df_tab=pd.read_csv('migration',header=None)	#reading the csv file
	
	df_tab.to_csv(sys.stdout)		#display in csv format
    
	df1=df_tab.drop(df_tab.index[85:],axis=0)		#splitting the table for Number part
	df2=df_tab.drop(df_tab.index[:86],axis=0)		#splitting the table for percent part
    
	cname1=df1.iloc[1,1:10]		#extracting the first level column header
	cname2=df1.iloc[2,1:10]		#extracting the second level column header
	cname3=df1.iloc[3,1:10]		##extracting the third level column header
	cname4=df1.iloc[4,:1]		#extracting the word Number
	
	cname1.replace(np.nan,' ',inplace=True)		#replacing the NaN values by space
	cname2.replace(np.nan,' ',inplace=True)
	cname3.replace(np.nan,' ',inplace=True)
	
	iname=df_tab.iloc[1,:1]		#extracting the index name Mobility Period
	
	iterables=[cname1,cname2,cname3]
	tuples=list(zip(*iterables))		#Made tthe column header values as a tuple for multi indexing.check the output for
										#cname1,cname2,cname3,tuples
	
	df1.drop([0,1,2,3,4,5],axis=0,inplace=True)	#remove the rows above the data
	df1.drop([10],axis=1,inplace=True)		#remove the last NaN column
	
	df1.set_index([0],inplace=True)		#setting first column as index
	df1.columns=pd.MultiIndex.from_tuples(tuples)	#multiindexing the columns with tuple values
	
	df1.index.names=iname		#naming the index
	
	df1.dropna(inplace=True)  #dropping null vvalues
	df1.head(10)
	
	#reshaping the table
	df1=df1.stack()
	df1=df1.stack()
	df1=df1.stack()
	
	df1=DataFrame(df1,columns=['NUMBER']) 	#naming the value column
	df1=df1.swaplevel(-3,-1,axis=0)	#ordering the indexes
	
	df1.sort_index(level=-4,axis=0,ascending=True,inplace=True)	#sorting the index
	
	df1.index.rename(['Total','Different Residence','Different County'],level=[-3,-2,-1],inplace=True) 	#renaming the indexes which left unnamed
	df1.head(20)
	
	#repeating all the steps for df2
	cname5=df2.iloc[0,:1]
	
	df2.drop([86,87],axis=0,inplace=True)
	df2.drop([10],axis=1,inplace=True)
	
	df2.set_index([0],inplace=True)
	df2.columns=pd.MultiIndex.from_tuples(tuples)
	
	df2.index.names=iname
	
	df2.dropna(inplace=True)
	df2.head(10)
	
	
	df2=df2.stack()
	df2=df2.stack()
	df2=df2.stack()
	df2=DataFrame(df2,columns=['PERCENT'])
	
	df2=df2.swaplevel(-3,-1,axis=0)
	
	df2.sort_index(level=-4,axis=0,ascending=True,inplace=True)
	
	
	df2.index.rename(['Total','Different Residence','Different County'],level=[-3,-2,-1],inplace=True)
	df2.head(20)
	
	#joining the two tables to get the final table
	df_tab=df1.join(df2)
	
	df_tab
	#exporting to csv file
	df_tab.to_csv('cleaned_migration.csv')
if (myCSV=="MedianIncome"):
	df_mincome=pd.read_csv('MedianIncome.csv',header=None)		#reading the csv file
	df_mincome.to_csv(sys.stdout)			#display in csv format
	
	df1=df_mincome.drop(df_mincome.index[56:],axis=0)		#splitting the table for current dollars part
	df2=df_mincome.drop(df_mincome.index[:56],axis=0)		#splitting the table for 2017 dollars part
	
	cname1 =list(df1.iloc[1,:1])	#extracting the first level column header
	cname2=list( df1.iloc[2,1:])	#extracting the second level column header
	cname3=list(df1.iloc[3,1:])		#extracting the third level column header
	inames = list(df1.iloc[2,:1])		#extracting the index name State
	
	cname1=cname1*len(cname3)		#make the number of elements in all the column header lists equal.
	iterables=[cname1,cname2,cname3]
	tuples=list(zip(*iterables))		##Made tthe column header values as a tuple for multi indexing.check the output for
										#cname1,cname2,cname3,tuples
	df1.drop([0,1,2,3],axis=0,inplace=True)	#remove the rows above the data
	
	
	df1.set_index([0],inplace=True)	#setting first column as index
	df1.columns = pd.MultiIndex.from_tuples(tuples)		#multiindexing the columns with tuple values
	
	df1.index.names = inames		#naming the index
	df1
	
	#repeating all the steps for df2
	cname1 =list(df2.iloc[0,:1])
	cname2=list( df2.iloc[1,1:])
	cname3=list(df2.iloc[2,1:])
	inames = list(df2.iloc[1,:1])
	
	cname1=cname1*len(cname3)
	iterables=[cname1,cname2,cname3]
	tuples=list(zip(*iterables))
	
	df2.drop([56,57,58],axis=0,inplace=True)
	
	
	df2.set_index([0],inplace=True)
	df2.columns = pd.MultiIndex.from_tuples(tuples)
	
	df2.index.names = inames
	df2
	
	#joining the two tables to get the final table
	df_mincome=df1.join(df2)
	df_mincome=df_mincome.rename_axis(['Rate','Year','Aspect'], axis=1)	#renaming the unnamed indexes
	df_mincome
	
	#reshaping the table
	df_mincome=df_mincome.stack()
	df_mincome=df_mincome.stack()
	df_mincome=df_mincome.stack()
	
	df_mincome=df_mincome.unstack(level=-4)	#making States as column headers
	
	df_mincome=df_mincome.swaplevel(-3,-1,axis=0)	#reordering the indexes
	
	#replace odd year entries with plain to allow for data sorting
	
	df_mincome.sort_index(axis=0,level='Rate',ascending=False,inplace=True)	#sorting the index
	
	#final table
	df_mincome
	#exporting to csv file
	df_mincome.to_csv('cleaned_medianIncome.csv')
if (myCSV=="education.xlsx"): ###<----------ZHENG ENTER YOUR ORIGINAL FILE NAME HERE
	df = pd.read_excel('education.xlsx',
		          skiprows=5,
		          header=[0,1],
		          skipfooter=13,
		          useclos=10,
		          na_values='(NA)',
		          index_col=[0,1,2,3])
	# Put the value of Median from top to the column 
	df = df.set_index([('Median','Unnamed: 10_level_1')], append=True)
	# drop the Nah values of all the foramt 
	df.dropna(how = 'all', inplace=True)
	# using stack. stack to extract the sex, year, and age separately and set them into different column
	df= df.stack().stack()
	#Switch whole index to columns 
	df=df.reset_index()
	#Rename each column
	df.rename(columns={ 'Age, sex, and years': 'Age',
		            'Unnamed: 1_level_2': 'sex',
		            'Unnamed: 2_level_2': 'year',
		            df.columns[4] : 'median',
		            df.columns[5] : 'year_level',
		            df.columns[6] : 'school_level',
		            df.columns[7] : 'number_of_people'},
		      inplace = True)
	#output the data and remove the index 
	df.to_csv('cleaned_education.csv', index= False)