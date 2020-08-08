if __name__ == '__main__':

	import numpy as np
	import pandas as pd
	import plotly as pl
	import plotly.express as px
	import plotly.graph_objs as go
	from plotly.subplots import make_subplots
	from plotly.offline import download_plotlyjs, plot, iplot

	'''
	Prepare data
	'''
	
	# Read data
	# 1. Covid-19 cases and deaths, daily, from Center for Systems Science and Engineering (CSSE) at Johns Hopkins University:
	#	 https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset/data?select=covid_19_data.csv
	# 2. Countries' populations (in 2019), from World Bank:
	#	 https://data.worldbank.org/indicator/SP.POP.TOTL
	df = pd.read_csv(r".\data\covid_19_data2.csv")
	pops = pd.read_csv(r".\data\world population.csv", header=2)

	# Rename columns
	df = df.rename(columns={'Country/Region':'Country', 'ObservationDate':'Date'});
	pops = pops.rename(columns={'Country Name':'Country', '2019':'Population'})
		
	# Select columns
	pops = pops[['Country', 'Population']]

	# Align datasets
	# (This was done manually using the commented-out code below)
	df_countries = np.unique(df.Country)
	len(df_countries) # 223
	pops_countries = np.unique(pops.Country)
	len(pops_countries) # 264
	np.setdiff1d(df_countries, pops_countries) # Prints countries listed in df but not pops
	np.setdiff1d(pops_countries, df_countries) # Prints countries listed in pops but not df
	pops = pops.replace({'Brunei Darussalam':'Brunei',
						 'Congo, Dem. Rep.':'Congo (Kinshasa)',
						 'Egypt, Arab Rep.':'Egypt',
						 'Hong Kong SAR, China':'Hong Kong',
						 'Iran, Islamic Rep.':'Iran',
						 "Cote d'Ivoire":'Ivory Coast',
						 'Kyrgyz Republic':'Kyrgyzstan',
						 'Lao PDR':'Laos',
						 'Macao SAR, China':'Macau',
						 'China':'Mainland China',
						 'Myanmar':'Burma',
						 'Congo, Rep.':'Republic of the Congo',
						 'Russian Federation':'Russia',
						 'St. Kitts and Nevis':'Saint Kitts and Nevis',
						 'St. Lucia':'Saint Lucia',
						 'St. Vincent and the Grenadines':'Saint Vincent and the Grenadines',
						 'Slovak Republic':'Slovakia',
						 'Korea, Rep.':'South Korea',
						 'Syrian Arab Republic':'Syria',
						 'Caribbean small states':'The Bahamas',
						 'United Kingdom':'UK',
						 'United States':'US',
						 'Venezuela, RB':'Venezuela',
						 'Yemen, Rep.':'Yemen'})
	countries = list(set(np.unique(df.Country)) & set(np.unique(pops.Country))) # intersection
	df_density = df[df['Country'].isin(countries)] # Keep only rows with countries in both lists
	
	'''
	Preprocess data
	'''

	# Remove Qatar because it's an outlier that throws off color scheme but is too small to see on choropleth
	df_density = df_density[df_density['Country'] != 'Qatar']

	# Group data by country and sort by date
	df_date = df[df['Confirmed']>0]
	df_date = df_date.groupby(['Date','Country']).sum().reset_index()	

	# Create 'Case Rate' column representing % of population with confirmed cases
	df_date = pd.merge(df_date, pops, on='Country', how='left')
	df_date['Case Rate'] = df_date['Confirmed'] / df_date['Population'] * 100

	# Calculate and create columns:
	# 1. 'Mortality Rate': % of confirmed cases that ended in fatality
	# 2. 'Mortality Rate / Pop.': Mortality rate divided by population
	# 3. 'Mortality Rate by Covid Rate': Mortality rate divided by % of population with reported cases
	df_date['Mortality Rate'] = df_date['Deaths'] / df_date['Confirmed'] * 100
	
	# 
	df_date2 = df_date[df_date['Population'] > 0]
	df_date2['Mortality Rate / Pop.'] = df_date2['Mortality Rate'] / df_date2['Population']
	# Remove San Marino and Antigua and Barbuda because they're outliers that throw off color scheme but are too small to see on choropleth
	#df_date2 = df_date2[df_date2['Country'] != ['San Marino', 'Antigua and Barbuda']]
	df_date2 = df_date2[~(df_date2['Country'].isin(['San Marino', 'Antigua and Barbuda']))]

	#
	df_date3 = df_date[df_date['Case Rate'] > 0]
	df_date3['Mortality Rate / Case Rate'] = df_date3['Mortality Rate'] / df_date3['Case Rate']
	
	print(df_date2.groupby(['Country']).max().reset_index().sort_values(by=['Mortality Rate / Pop.'], ascending=False))
	print(df_date3.groupby(['Country']).max().reset_index().sort_values(by=['Mortality Rate / Case Rate'], ascending=False))
	#print(df_date2.sort_values(by=['Mortality Rate / Pop.'], ascending=False))
	#print(df_date3.sort_values(by=['Mortality Rate / Case Rate'], ascending=False))
	
	# Calculate all-time stats (averaged over time)

	'''
	Make figure
	'''
	
	choro1 = px.choropleth(df_date,
						   locations='Country',
						   locationmode='country names',
						   color='Confirmed',
						   labels={'Confirmed':'Confirmed Cases'},
						   hover_name='Country',
						   animation_frame='Date')
	choro1.update_layout(title_text='Confirmed Covid-19 Cases',
					     title_x=0.5,
					     geo=dict(showframe=False, showcoastlines=False))
	choro1.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
	
	choro2 = px.choropleth(df_date,
						   locations='Country',
						   locationmode='country names',
						   color='Case Rate',
						   labels={'Case Rate':'Case Rate (%)'},
						   hover_name='Country',
						   animation_frame='Date',
						   range_color=[0,1.7])
	choro2.update_layout(title_text='Confirmed Covid-19 Cases',
						 annotations=[dict(x=0.53,y=1.05,showarrow=False,text='(% of population reported with confirmed cases)')],
					     title_x=0.5,
					     geo=dict(showframe=False, showcoastlines=False))
	choro2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
	
	choro3 = px.choropleth(df_date,
						   locations='Country',
						   locationmode='country names',
						   color='Mortality Rate',
						   labels={'Mortality Rate':'Mortality Rate (%)'},
						   hover_name='Country',
						   hover_data=['Deaths'],
						   animation_frame='Date',
						   range_color=[0,10])
	choro3.update_layout(title_text='Covid-19 Mortality Rate',
						 annotations=[dict(x=0.54,y=1.05,showarrow=False,text='(% of confirmed cases resulting in fatality)')],
					     title_x=0.5,
					     geo=dict(showframe=False, showcoastlines=False))
	choro3.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
	
	choro4 = px.choropleth(df_date2,
						   locations='Country',
						   locationmode='country names',
						   color='Mortality Rate / Pop.',
						   hover_name='Country',
						#   hovertemplate = '<b><u>%{Country}</u></b><br>' +
						#				   '<br><b>Mortality Rate:</b> %{Mortality Rate:.2f}' +
						#				   '<br><b>Population:</b> %{Population:.2f}' +
						#				   '<br><b>Mortality Rate / Pop.:</b> %{Mortality Rate / Pop.:.2f}',
						#   hover_data={'Mortality Rate':True},
						#			   'Mortality Rate':':.2f',
						#			   'Population':':.2f',
						#			   'Country':False,
						#			   'Mortality Rate / Pop.':':.2f'},
						   hover_data=['Mortality Rate', 'Population'],
						   animation_frame='Date',
						   range_color=[0,0.000001])
	choro4.update_layout(title_text='Covid-19 Mortality Rate / Pop.',
					     title_x=0.5,
					     geo=dict(showframe=False, showcoastlines=False))
	choro4.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
		
	choro5 = px.choropleth(df_date3,
						   locations='Country',
						   locationmode='country names',
						   color='Mortality Rate / Case Rate',
						   hover_name='Country',
						#   hover_data={'Mortality Rate':':.2f',
						#			   'Case Rate':':.2f',
						#			   'Country':False,
						#			   'Mortality Rate \ Case Rate':':.2f'},
						   hover_data=['Mortality Rate', 'Case Rate'],
						   animation_frame='Date',
						   range_color=[0,1000])
	choro5.update_layout(title_text='Covid-19 Mortality Rate / Case Rate',
					     title_x=0.5,
					     geo=dict(showframe=False, showcoastlines=False))
	choro5.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
	
	choro1.show()
	choro2.show()
	choro3.show()
	choro4.show()
	choro5.show()

	'''
	STATIC:

	# Organize data
	df_countries = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date', ascending=False)
	df_countries = df_countries.drop_duplicates(subset = 'Country')
	df_countries = df_countries[df_countries['Confirmed']>0]

	# Create static choropleth
	fig = go.Figure(data=go.choropleth(locations=df_countries['Country'],
										locationmode='country names', 
										z=df_countries['Confirmed'],
										colorscale='Reds',
										marker_line_color='black',
										marker_line_width=0.5))
	fig.update_layout(title_text='Confirmed Cases',
					  title_x=0.5,
					  geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
	'''
