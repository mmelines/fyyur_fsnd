What is actually happening?

1. with `python3 populate.py`, `__name__=="__main__"` is called and
	1. First, `ThinData(True)` constructor creates blank global object
		- parameter `True` ensures global object is created blank at first
	2. Then, `CliCtl()` constructure creates cli interaction object
		- 

2. So within `ThinData(True)`:
	- `self.model()` makes a blank singleton object for the entire model
		& what's in it? 
		* blank lists of all things that are going to be created:
			- `"artists"`
			- `"shows`
			- `"venues`
		* an object called `model[<location>]` for each model in the list of locations stored in the program

			```
				 {'venues', {},
					'venue_ids': [],
					'artists': {},
					'artist_ids': [],
					'shows': }
			```
	
		- on a broader note, what is happening is that we have a relationship modeled in our db with a relational table `show` between `artist` and `venue`, represented by the PK of each (`artist.id`, `venue.id`)
		- more specifically, we are limiting the creation of this false data to selections within a third criteria (location) and this criteria does not exist in a foreign table. The unique identifier is just the city name, which we know to be unique because of a limited list of cities listed in the `RdDb` class (random database class)

3. Then, once we have a blank singleton object that's sorted by this arbitrary limitation, we check to see if the list of `genres` specified by 
