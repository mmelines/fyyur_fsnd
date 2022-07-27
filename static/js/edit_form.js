const init_existing = function() {
	// populate form with the entity's existing values from database query
	for (let attribute of Object.keys(entity)) {
		if (!["genres", "id", "shows", "has_image", "is_seeking", "past_shows", "upcoming_shows", "availability"].includes(attribute)) {
			form_div = document.getElementById(attribute);
			if (form_div) {
				form_div.value = entity[attribute];
			} else {
				console.log("WARN did not locate " + attribute);
			}
		}
	}
}

const select_genre = function(genre_name, genre_id, add_genre) {
	// select genre in hidden select multiple container programatically
	option = document.querySelector('select.hidden option[value="' + genre_name + '"]');
	if (Object.keys(genres).includes(genre_id)){
		if (add_genre) {
			option.selected = true;
		} else {
			option.selected = false;
		}
	}
	genre_select = document.getElementById('genres');
}

const init_genre_element = function() {
	// ensure all genres from entity's db query are selected on page load
	for (genre_option in document.getElementById('genres').options) {
		console.log("for:");
		console.log(genre_option)
		genre_id = genre_option.index;
		if (Object.values(current_genres).includes(genre_option)) {
			select_genre(genres[genre_option], genre_option, true);
		} else {select_genre(genres[genre_option], genre_option, false);}
	}
}

const init_genre_display = function() {
	// alter visible genre div to show green background for genres in entity's db query
	current_genres = {}
	// change display of genre_elements
	for (genre_div in genre_elems) {
		// get name and id from element
		const div = genre_elems[genre_div];
		const id = div.id;
		// change class of genre element
		if (div.innerText != undefined)
		{
			const name = div.innerText;
			if (entity.genres.includes(name)) {
				console.log("alter for " + name);
				div.classList.remove("unsel-gen");
				div.classList.add("sel-gen");
				current_genres[name] = id;
			} else {console.log("neg eval for " + name);}
			div.addEventListener('click', function() {toggle_genre(div, id, name)});
		}
	}
	return current_genres;
}

const shift_genres = function() {
	// change genre id from database to a key that matches array index of genres selectMultiple
	for (genre_index in genres) {
		indexed_name = genres[genre_index]["name"];
		genre_option_index = document.querySelector('select.hidden option[value="' + indexed_name + '"]').index;
		genres[genre_option_index] = indexed_name;
		delete genres[genre_index];
		genre_element = document.getElementById(genre_index);
		genre_element.id = genre_option_index;
	}
	return genres;
}

const init_genres = function() {
	// correct keys of db genres option
	genres = shift_genres();
	current_genres = init_genre_display();
	init_genre_element(current_genres);
	alter_current_genres(current_genres);
	return current_genres;
};

const alter_current_genres = function(genre_name, add_genre) {
	// update current genres string list for form submission
	cg_div = document.getElementById('current-genres');
	cg_text = "";
	for (genre in current_genres) {
		cg_text += genre + ", "
	}
	cg_div.innerText = cg_text.slice(0, -2);
};

const toggle_genre = function(div, id, name) {
	// change display of visible genre tags on click
	if (div.classList.contains('unsel-gen')) {
		// if genre is selected for the entity, change its style and remove it from selections
		div.classList.remove("unsel-gen");
		div.classList.add("sel-gen");
		current_genres[name] = id;
		add_genre = true;
	}
	else if (div.classList.contains('sel-gen')){
		// if genre is not selected for the entity, change its style and select it
		div.classList.remove("sel-gen");
		div.classList.add("unsel-gen");
		delete current_genres[name];
		add_genre = false;
	}
	// update selectMultiple genres object
	select_genre(name, id, add_genre);
	// update genres list (str)
	selected_genres = alter_current_genres(name, add_genre);
};

display_state_value = function() {
	// display existing state of entity in dropdown menu at page load
	document.getElementById('state').value = entity.state;
};

display_seeking_value = function() {
	// display accurate value of 'seeking_venues' onload
	if (entity.is_seeking == true) {
		document.getElementById(is_seeking).checked = true;
	};
};

const presubmit = function(e) {
	// add string genres_list to form object before form submission
	// corrects error re: genres selectMultiple intermittently returning only first genre
	thisform = document.forms[0];
	current_values = document.getElementById('current-genres').innerText;
	var final_genre_list = document.createElement("input");
	final_genre_list.type = "text";
	final_genre_list.name = "genres_string";
	final_genre_list.id = "genres_string";
	final_genre_list.value = current_values;
	thisform.append(final_genre_list);
	image_url = document.getElementById('image_link').value;
	var final_has_image = document.createElement("input");
	final_has_image.type = "checkbox";
	final_has_image.name = "has_image";
	final_has_image.id = "has_image";
	final_has_image.checked = (image_url.length > 0)?true:false;
	thisform.append(final_has_image);
}

window.onpageshow = function() {
	console.log("load window"); // confirm this script is linked properly
	entity = false;
	try {
		// if artist is recieved, set entity to artist and add required attributes
		entity = artist;
		entity_type = "artist";
		is_seeking = 'seeking_venue';
		endpoint = '/artists/'+entity.id;
	} catch(e) {};
	try {
		// if venue is recieved, set entity to venue and add required attributes
		entity = venue;
		entity_type = "venue";
		is_seeking = 'seeking_artist';
		endpoint = '/venues/'+entity.id;
	} catch(e) {};
	// populate form elements with existing values if entity recieved is a string
	if (!entity==false) {
		init_existing();
		genre_elems = document.getElementsByClassName('genre-container');
		current_genres = init_genres();
		display_state_value();
		display_seeking_value(is_seeking);
	}
}

