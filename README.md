### PUR BEURRE PROGRAM

Author : VERNHES Cyril

#### Description :

This program allows you to search for a substitute and save it in favorites.
Products are downloaded from the database Openfoodfacts.

#### Prerequisites :

To work, the program requires python 3.

#### Start program and virtual environment : 

Download the project with Git and open the command line and go to project path :

###### Create the directory of virtualenv files named venv :
`python3 -m venv venv`

###### Activate the virtual environment
`venv\Scripts\activate.bat`

###### Install the libraries
`pip install -r requirements.txt`

###### Download products
`python3 manage.py openfoodfacts`
or
`python3 manage.py openfoodfacts --delete`
for deleting database


###### Start test server :
`python3 manage.py runserver`

###### Stop virtual environment :
`deactivate`

#### Configurations :

You can change the categories and the maximum number of products downloaded in the files named : config/config.py

#### Controls :

To access to the desired menu, simply type the number corresponding to your choice.

Press "q" to return to the main menu.
Press "s" or "p" in the product menu and in the substitute menu for navigate.
Press "y" or "n" to validate or not the registration of the substitute product.