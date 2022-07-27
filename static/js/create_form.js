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

// ----------------------------------------------------------------

const is_avail = function(target, index) {
	availability[index] = true;
	if (target.classList.contains('avail-false')){
		target.classList.remove('avail-false');
	};
	target.classList.add('avail-true');
}

const not_avail = function(target, index) {
	availability[index] = false;
	target.classList.remove('avail-true');
	target.classList.add('avail-false');
}

const toggle_availability = function(event) {
	index = event.target.id.slice(-1, );
	if (event.target.classList.contains('avail-true')) {
		not_avail(event.target, index);
	} else if (event.target.classList.contains('avail-false')) {
		is_avail(event.target, index);
	}
} 

const init_availability = function() {
	console.log("init availability called");
	for (let i=0; i<7; i++) {
		var elem = document.getElementById("avail-"+i);
		elem.addEventListener('click', (event) => {toggle_availability(event)});
		if (elem.classList.contains('avail-true')) {
			availability[i] = true;
		};
		if (elem.classList.contains('avail-false')) {
			availability[i] = false;
		}
		if ((!elem.classList.contains('avail-true') && 
			(!elem.classList.contains('avail-false')))) {
				is_avail(elem, i);
			};
	};
	console.log(availability);
}

const presubmit = function(e) {
	// add string genres_list to form object before form submission
	// corrects error re: genres selectMultiple intermittently returning only first genre
	
	function append_genres() {
		// process select genres and add them to list
		current_values = document.getElementById('current-genres').innerText;
		var final_genre_list = document.createElement("input");
		final_genre_list.classList.add("hidden");
		final_genre_list.type = "text";
		final_genre_list.name = "genres_string";
		final_genre_list.id = "genres_string";
		final_genre_list.value = current_values;
		thisform.append(final_genre_list);
		return final_genre_list;
	}

	function append_availability() {
		console.log(availability);
		var week = [];
		for (let i=0; i<7; i++) {
			week[i] = availability[i];
		}
		console.log(week);
		var artist_avail = document.createElement("input");
		artist_avail.classList.add("hidden");
		artist_avail.type="text";
		artist_avail.name = "artist_availability";
		artist_avail.id = "artist_availability";
		artist_avail.value = week;
		return artist_avail;
	};
	
	thisform = document.forms[0];
	thisform.append(append_genres());
	if (document.getElementById('avail-container')) {
		thisform.append(append_availability());
	}
}

var availability = {}
window.onpageshow = function() {
	console.log("load window"); // confirm this script is linked properly
    genre_elems = document.getElementsByClassName('genre-container');
    current_genres = init_genres();
	// implement availability event functions 
	if (document.getElementById('avail-container')) {
		console.log("has_availability");
		init_availability();
	} else {
		console.log("doesn't have any availability");
	}
}

