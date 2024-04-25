  •	data_prep_prep.py:
    o	remove_repeated_headers
        This function removes repeated headers from the Pandas DF
    o	calculate_fantasy_points
      	This function takes the fantasy relevant columns, does the math, and produces a fantasy points column
    o	convert_percent_to_float
      	converts all percent numbers into float versions of the same percentage
    o	round_dataframe
      	rounds the numeric data to the hundredths place
    o	process_and_merge
      	processes using the above helper functions, then makes merged training and testing datasets
 •	data_preparation.py:
    o	load_data
      	loads a csv into dataframe
    o	create_sequences
      	creates sequences to be loaded into the model
 •	dataset.py:
    o	__init__
    o	__len__
    o	__getitem__
    
 •	GUI.py:
    o	__init__ 
    o	scrape
      	runs the scrape script
    o	clearCache
      	currently does not delete data, not sure if this function will be necessary going forward
    o	genRankings
      	runs the create_rankings function in main and loads the table
    o	modPopup
      	modifies scoringconfig 
    o	arcPopup
      	popup to load 
    o	loadTable
      	loads csv into the gui
    o	readScoringConfig
      	reads the scoring config into the mod popup
    o	writeScoringConfig
      	takes the mod popup and writes to scoring conifg
•	main.py:
    o	main
      	purely for tests and training
    o	load_model_and_scalers
      	helper function to load the models and scalers 
    o	predict
      	predicts based on loaded models and scalers
    o	create_and_train
      	creates various necessary models and calls train functions
    o	create_ranking
      	takes the prediction function and creates a csv of a ranking
 •	model.py:
    o	__init__
    o	forward
 •	Webscraper.py/WebScraper Experts:
    o	main
    o	__init__
    o	get_html_content
      	uses bs4 to scrape the html
    o	get_table
      	gets the necessary table from the html
    o	get_headers
      	grabs table headers
    o	get_rows
      	grabs table rows
    o	get_dataframe
      	creates a dataframe from the data
    o	scrape_table_to_csv
      	saves the dataframe to csv
