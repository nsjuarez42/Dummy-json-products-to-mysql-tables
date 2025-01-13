# Mysql dump from the dummy json data for products 
The following repo consists of several files
- **fetchadata.py**: used to fetch the data and write it to the data.json file
- **data.json**: The file containing all the data in json format saved in plain text
- **create mysql database.py**: The file containing the program that creates the database and fills it with the data from the **data.json** file
- **products_dump.mysql**: The resulting dump from the database created with the **create mysql database.py** file.
- **requirements.txt**: The necessary pip packages needed in order to run the **create mysql database.py**