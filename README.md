# Nor'Easter

LINK TO VIDEO: https://youtu.be/Q7EvlQkvq2M

INTRODUCTION
    This project is a website called Nor'Easter, created using the Flask framework to be able to pass server requests to the web applications.The main function of this website is to allow a user to search for a certain ski resorts in New England, stored in the folder in a database named "skiing.db", in the two tables labelled "resorts" and "runs". A user should then be able to store a certain ski resort into their own checklist, thus allowing the user to submit certain mountains back into a separate table of the "skiing.db" database, called "checklist".

COMPILING AND RUNNING
    The process to compile and run the web application is through starting a development server in a user's terminal. Once this folder is downloaded, ensure that there are three main folders, "flask_session", "static", and "templates", along with the main "app.py" file, the "helpers.py" file, and the database file "skiing.db". The static folder should contain a JavaScript file (script.js), a CSS file (styles.css) and a .geojson file (skiing_areas.geojson). The "templates" folder should contain seven different .html pages: "checklist", "index", "layout", "login", "map", "reigster", and "search".

    In the terminal, access the directory of the folder using "cd noreaster", and once inside, start a development server by passing the command "flask run" into the terminal, which should output a link to direct the user to the website.

USING THE WEB APPLICATION
    If compiling and running the web application was successful and the link is clicked, the user should be now on the homepage of the website. From there, the user may click around the various features and pages that the web application has to offer. As a note, to be able to access the checklist page, the user must be logged into an account, which can be easily done by clicking on the register button a creating an account.

INSIDE skiing.db
    The database file skiing.db is the main file that stores all the data and information in the web application to be used. Checking the schema of the file, there are 4 different tables: "users", "resorts", "runs", and "checklist". The "users" table stores the id, username, and hashed password of all the registered users in the website. The "resorts" and "runs" tables contain the information found in the skiing_areas.geojson file to be used accessibly. "resorts" holds the the ski resort's unique id, its name, operating status, and some basic information such as elevation levels and region/state. "runs" holds the amount of trails of each difficulty that exists for each resort, along with some basic information about it as well. Finally, the "checklist" table contains each item that is added to a user's checklist, which is organized using the resorts' and users' unique id's, along with storing a unique comment for each of the checklist items.

INSIDE skiing_areas.geojson
    The skiing_areas.geojson is a special type of JSON file that also contains coordinates and geometry that shows the location of a certain item. In this .geojson file contains all the information that was used inside the skiing.db database in the "resorts" and "runs" tables, which is then displayed in the web application. This .geojson file was retrieved from the OpenSkiMap website, which can be found here: https://openskimap.org/?about . The information from the website was then sorted to only contain the resorts from Massachusetts, Vermont, New Hampshire, and Maine.

INSIDE helpers.py
    Helpers.py is an additional python script that is imported in the main "app.py" script, which mainly contains the helper functions "login_required". This function basically allows for the implementation of checking whether the user is logged into an account or not. If the user is logged in, then the code will continue as normal. If the user is not logged in, then they will be redirected to the login page.
