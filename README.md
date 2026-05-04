### INF601 - Advanced Programming in Python
### Corbin Luck
### Final Project
 
 
# National Vulnerability Database Lookup
 
A website that parses through the National Vulnerability Database and returns searches based on keywords
 
## Description
 
There are three tabs on the website: Lookup, Low-Severity, and Donations. The Lookup page is where you can search
through the database based on keywords such as apache, windows, ect. The Low-Severity page parses through 2000 entries
and orders them based on the lowest severity providing a description for them. The Donations page is a mock donations 
page that is found on many free to use websites.
 
## Getting Started
 
### Dependencies

* This project was tested on a Window 11 machine, other OS systems may or may not work
* It was also created in Python version 3.14, it is unknown if it will work in older or newer versions

Please install the pip requirements:
```
pip install -r requirements.txt
```
 
### Installing
 
* Click to the <> Code button at the top of the page
* Copy the web URL after selecting HTTPS
* Using a program such as Pycharm clone the repository using the link you copied
* If you haven't already install the requirments folder using the command above
 
### Executing program
 
* After cloning the repository you will want to run the following command below
  * Note that to update any changes to the website the session will need to be shutdown if a flask server is not being
  used
```
flask --app flaskr run --debug
```
* Next you click on http://127.0.0.1:5000 link to open the project in your browser
* Finally click in the search tab on the website to filter by keywords

## Authors
 
Corbin Luck
 
## Version History
 
* 0.1
    * Initial Release
 
## License
 
N/A
 
## Acknowledgments
 
Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [Flask](https://flask.palletsprojects.com/en/stable/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [Matplotlib](https://matplotlib.org/stable/users/getting_started/)