const init_existing = function() {
	for (let attribute of Object.keys(entity)) {
		if (!["genres", "id", "shows", "has_image", "is_seeking"].includes(attribute)) {
			form_div = document.getElementById(attribute);
			form_div.value = entity[attribute];
		}
	}
}

const select_genre = function(genre_name, genre_id, add_genre) {
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
	for (genre_option in document.getElementById('genres').options) {
		genre_id = genre_option.index;
		if (Object.values(current_genres).includes(genre_option)) {
			select_genre(genres[genre_option], genre_option, true);
		} else {select_genre(genres[genre_option], genre_option, false);}
	}
}

const init_genre_display = function() {
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
				div.classList.remove("unsel-gen");
				div.classList.add("sel-gen");
				current_genres[name] = id;
			}
			div.addEventListener('click', function() {toggle_genre(div, id, name)});
		}
	}
	return current_genres;
}

const shift_genres = function() {
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
	genres = shift_genres();
	current_genres = init_genre_display();
	init_genre_element(current_genres);
	alter_current_genres(current_genres);
	return current_genres;
}

const alter_current_genres = function(genre_name, add_genre) {
	//
	cg_div = document.getElementById('current-genres');
	cg_text = "";
	for (genre in current_genres) {
		cg_text += genre + ", "
	}
	cg_div.innerText = cg_text.slice(0, -2);
}

/*
const alter_genres = function() {
	// recieve add_genre bool as new_value and set value of genre list to new_value
	option = document.querySelector('select.hidden option[value="' + genre + '"]');
	sel_genre = option.value;
	option.value = add_genre;
}
*/
const toggle_genre = function(div, id, name) {
	// if genre is selected for the entity, change its style and remove it from selections
	if (div.classList.contains('unsel-gen')) {
		div.classList.remove("unsel-gen");
		div.classList.add("sel-gen");
		current_genres[name] = id;
		add_genre = true;
	}
	// if genre is not selected for the entity, change its style and select it
	else if (div.classList.contains('sel-gen')){
		div.classList.remove("sel-gen");
		div.classList.add("unsel-gen");
		delete current_genres[name];
		add_genre = false;
	}
	select_genre(name, id, add_genre);
	selected_genres = alter_current_genres(name, add_genre);
}

display_state_value = function() {
	// display existing state of entity in dropdown menu at page load
	document.getElementById('state').value = entity.state;
}

display_seeking_value = function() {
	// display accurate value of 'seeking_venues' onload
	if (entity.is_seeking == true) {
		document.getElementById(is_seeking).checked = true;
	};
}

get_changes = function() {
	entity_form = {};
	for (let attribute in Object.keys(entity)) {
		key = Object.keys(entity)[attribute];
		try {
			form_element = document.getElementById(key);
			if (!["shows", "genres", "is_seeking"].includes(key)){
				console.log("   DO IT");
				let new_element = (form_element != null)?form_element:false;
				element_value = (new_element.value)? new_element.value :null;
				final_value = (element_value == null)?entity[key]:element_value;
			}
			if (key=="is_seeking") {
				final_value = document.getElementById(is_seeking).checked;
			}
			if (key=="genres") {
				genres_list = [];
				genres_object = document.getElementById('genres').selectedOptions;
				for (let genre_index in Object.values(genres_object)) {
					final_genre = genres_object[genre_index].value
					if (Object.values(genres).includes(final_genre)){
						genres_list.push(final_genre);
					}
				}
				unchanged_genres = true;
				if (genres_list.length == entity.genres.length) {
					for (let genre of entity.genres) {
						if (!genres_list.includes(genre)){
							unchanged_genres = false;
						}
					}
					final_genres_list = (unchanged_genres==false)?genres_list:entity.genres;
				} else {
					unchanged_genres = false;
					final_genres_list = genres_list;
				}
				final_value = entity[key];
				if (unchanged_genres == false){
					genres_string = "";
					for (let genre of final_genres_list) {
						genres_string += genre + ", "
					}
					final_value = (genres_string.length > 0)?genres_string.slice(0, -2):"";
				}
			}
			if (key=="shows") {final_value=null;}
		}
		catch (e) {
			new_value = null;
			final_value = new_value;
			console.log(key + e)}
		finally {
			if (final_value != null) {
				if (final_value != entity[key]) {
					entity_form[key] = final_value
				}
			}
		}
	}
	return entity_form;
}

finalize_entity = function(entity_form) {
	let purpose = (document.getElementById('submit-btn').value.includes('Edit'))?'edit':'create';
	entity_form['process'] = purpose;
	entity_form['entity_type'] = entity_type;
	entity_form['id'] = entity.id;
	endpoint += "/" + purpose + "/";
	return entity_form;
}

submit_form =function() {
	entity_form = finalize_entity(get_changes());
	const url = "/artists/edit/";
	const options = {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		mode: 'no-cors',
		body: JSON.stringify(entity_form)
	}
	console.log("try fetch: [" + url + "]");
	console.log(options);
	fetch(url, options)
		.then(res=> res.json())
		.then(res=>{console.log(res)});
	console.log("fetch'd");
}

async_submit = function(e) {
	e.preventDefault();
	submit_form();
	console.log("async_submit not complete");
}

window.onpageshow = function() {
	console.log("load window");
	entity = false;
	try {
		entity = artist;
		entity_type = "artist";
		is_seeking = 'seeking_venue';
		endpoint = '/artists/'+entity.id;
	} catch(e) {};
	try {
		entity = venue;
		entity_type = "venue";
		is_seeking = 'seeking_artist';
		endpoint = '/venues/'+entity.id;
	} catch(e) {};
	if (!entity==false) {
		init_existing();
		genre_elems = document.getElementsByClassName('genre-container');
		entity.genres = entity.genres[0].split(",");
		current_genres = init_genres();
		display_state_value();
		display_seeking_value(is_seeking);
	}
}

