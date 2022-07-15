# TravellerSpace
Flask-Based Web App

## Features
- backend
	- using MySQL connector to execute queries
		- Has several advantages over using SQLAlchemy
			- practice writing raw SQL queries instead of relying on abstraction layer 
			- lower latency compared to queries executed by an ORM 
- homepage
	- dynamic webpage using JavaScript
	- external CSS library (font-awesome)
- registration
- login
	- flashes error message if credentials are invalid
