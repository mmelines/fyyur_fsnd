// declare date global
var eventTime = {
    'set_date': function(type) {
        const start_date = function() {
            new_date = new Date(eventTime.sdd[0], 
                                eventTime.sdd[1],
                                eventTime.sdd[2],
                                eventTime.stt[0],
                                eventTime.stt[1]);
            eventTime.start_dt = new_date;
            return new_date;
        };
        const end_date = function() {
            new_date = new Date(eventTime.edd[0], 
                                eventTime.edd[1],
                                eventTime.edd[2],
                                eventTime.ett[0],
                                eventTime.ett[1]);
            eventTime.end_dt = new_date;
            return new_date;
        };
        switch(type) {
            case ("start"):
                return start_date();
                break;
            case ("end"):
                return end_date();
                break;
            default:
                start_date();
                end_date();
        };
    },
    'unset': function(data) {
        /*
         {'type': ['date' | 'type' | 'full'],
            'position': ['start', 'end'],
            'source': <element>}
        */
        switch(data['type']) {
            case ('date' || 'full'):
                var _date = [1970, 0, 1];
                if (data["position"] == "start") {
                    eventTime.sdd = _date;
                    eventTime.start_date = false;
                };
                if (data["position"] == "end") {
                    eventTime.edd = _date;
                    eventTime.end_date = false;
                };
                if (data['type'] == 'date') {
                    break;
                };
            case ('time'):
                var _time = (data['position'] == 'end') ? [0, 1] : [0, 0];
                if (data["position"] == "start") {
                    eventTime.stt = _time;
                    eventTime.start_time = false;
                };
                if (data["position"] == "end") {
                    eventTime.ett = _time;
                    eventTime.end_date = false;
                };
        };
        eventTime.set_date(data["position"]);
        data["source"].value = "";
    },
    'set': function(data) {
        /*
        data = {'type': [time_array||time_string||
                          date_array||date_string,
                          duration, reset],
                'position: [start|end],
                'value': <input>, [date|type|full]
                'validation': <function>,
                'validated': bool
            }
        */
        var input_array;
        var input_string;
        var dt_array = [];
        var input_type;
        console.log(" ! >> called set() using: ");
        console.log(data);
        switch(data['type']) {
            default:
                console.log("input: " + data['value']);
                input = data["value"];
            case ("time_array"):
                input_array = data["value"];
                input_string = data["value"].join(":");
                input_type = "time";
                break;
            case ("time_string"):
                input_array = data["value"].split(":");
                input_string = data["value"];
                input_type = "time";
                break;
            case ("date_array"):
                input_array = data["value"];
                if (data["source"] == "form") {
                    input_array[1] -= 1;
                }
                input_string = data["value"].join("-");
                input_type = "date";
                break;
            case ("date_string"):
                input_array = data["value"].split("-");
                if (data["source"] == "form") {
                    input_array[1] -= 1;
                }
                input_string = data["value"];
                input_type = "date";
                break;
        };
        for (number in input_array) {
            dt_array.push(parseInt(input_array[number]));
        };
        console.log(dt_array);
        if (data['position'] == "start") {
            if (input_type == 'time') {
                eventTime.stt = dt_array;
                if (data['validated'] == true) {
                    eventTime.start_date = input_string;
                };
            };
            if (input_type == 'date') {
                eventTime.sdd = dt_array;
                if (data['validated'] == true) {
                    eventTime.start_date = input_string;
                };
            };
            input_dt = eventTime.set_date("start");
            console.log("start input dt: " + input_dt);
        };
        if (data['position'] == "end") {
            if (input_type == 'time') {
                eventTime.ett = dt_array;
                if (data['validated'] == true) {
                    eventTime.end_time = input_string;
                };
            }
            if (input_type == 'date') {
                eventTime.edd = dt_array;
                if (data['validated'] == true) {
                    eventTime.end_date = input_string;
                };
            }
            input_dt = eventTime.set_date("end");
            console.log("end input dt: " + input_dt);
        };
        var msg = "called eventTime.set on " + data["type"];
        msg += " (" + data["position"] + ") w/ res. " + input_dt;
    },
    'start': false,
    'start_time': false,
    'stt': [0, 00],
    'sdd': [1970, 0, 1],
    'start_dt': new Date(1970, 0, 1, 0, 00),
    'start_date': false,
    'end': false,
    'end_time': false,
    'ett': [0, 01],
    'edd': [1970, 0, 1],
    'end_dt': new Date(1970, 0, 1, 0, 00),
    'end_date': false,
    'all_day': false,
    'multi_day': false,
    'duration': {'hours': false,
                'minutes': false}
};

var new_event = {
    "venue_name": false,
    "venue_image_link": false,
    "artist_name": false,
    "artist_image_link": false
};

/* ----------------------------------------------------------------------
*  event listeners
* ---------------------------------------------------------------------- */

// onchange event listener for start_time and start_date
const acceptStart = function(event) {
    var data = {'type': false,
            'position': false,
            'value': event.target.value,
            'validation': null,
            'validated': false,
            'source': "form"};
    if (event.target.id == 'start_time') {
        data.type = 'time_string';
        data.position = 'start';
        eventTime.set(data);
        // TODO conditional block for duration validation
        confirmValidTime(event.target);
    } else if (event.target.id == 'start_date') {
        data.type = 'date_string';
        data.position = 'start';
        eventTime.set(data);
        if (validDate("start") !=false) {
            data.validated = true;
            eventTime.set(data);
            defaultEndDate(event.target);
            confirmValidTime(event.target);
        } else {
            data = {"position": "start",
                    "type": "date",
                    "source": event.target};
            eventTime.unset(data);
            warnInvalidTime("past", event.target);
        };
    };
    console.log(eventTime);
};

// onchange event listener for end_time
const acceptEndTime = function(event) {
    var data = {'type': "time_string",
            'position': "end",
            'value': event.target.value,
            'validation': null,
            'validated': false,
            'source': "form"};
    eventTime.set(data);
    console.log(eventTime);
    if (validDate("end") != false) {
        data.validated = true;
        eventTime.set(data);
        confirmValidTime(event.target, 'time-error');
    } else {
        data = {"position": "end",
                "type": "time",
                "source": event.target};
        eventTime.unset(data);
        warnInvalidTime("negative-duration", event.target);
    };
    console.log(eventTime);
};

//onchange event listener for end_date
const acceptEndDate = function (event) {
    var data = {'type': "date_string",
            'position': "end",
            'value': event.target.value,
            'validation': null,
            'validated': false,
            'source': "form"};
    eventTime.set(data);
    if (validDate("end") != false) {
        data.validated = true;
        eventTime.set(data);
        confirmValidTime(event.target);
    } else {
        data = {"position": "end",
                "type": "time",
                "source": event.target};
        eventTime.unset(data);
        warnInvalidTime("date-duration", event.target);
    };
};

/* ----------------------------------------------------------------------
*  toggle display functions for form load
* ---------------------------------------------------------------------- */
const toggleHiddenClass = function(class_name, visibility) {
    /*
    * show or hide elements of a class
    */
    members = document.getElementsByClassName(class_name);
    for(let i=0; i < members.length; i++) {
        if (visibility==true) {
            members[i].classList.remove('hidden');
        } else if (visibility==false) {
            members[i].classList.add('hidden');
        }
    }
}

const toggleTimeGroup = function(event) {
    /*
    * checkbox listener; shows or hides time group inputs
    */
    if (event.target.checked) {
        // event is not 'all day'
        toggleHiddenClass("time-group", false);
        setAllDayDuration("set");
    }
    else {
        // event is 'all day'
        toggleHiddenClass("time-group", true);
        setAllDayDuration("unset");
    }
}

const toggleMultiDay = function(event) {
    /*
    * checkbox listener; shows or hides end data inputs
    */
    if (event.target.checked) {
        // multi-day event
        toggleHiddenClass("end-date-group", true);
    }
    else {
        // not multi-day
        toggleHiddenClass("end-date-group", false);
    }
}
/* ----------------------------------------------------------------------
*  toggle display functions for event preview
* ---------------------------------------------------------------------- */
const previewArtist = function(artist_data) {
    var data = {"name": artist_data.name,
                "img": artist_data.img,
                "entity_type": "artist"};
}
const previewVenue = function(venue_data) {

}

/* ----------------------------------------------------------------------
*  user feedback functionality
* ---------------------------------------------------------------------- */
const toggleChildMsg = function(input) {
    /*
    {entity_type,
    div = event.target,
    parent = event.target.parentElement
    to-exist,
    success 
    }
    */
    existing = document.getElementsByClassName(input['entity_type'] + "-msg");
    if (existing.length > 0) {
        for(let i = 0; i < existing.length; i++) {
            existing[i].remove();
        }
    }
    //
    if (input['to_exist']==true) {
        if (input["success"]==false) {
            input['div'].value = "";
        };
        let new_div = document.createElement('div');
        let div_desc = (input['success'] == true) ? "-confirm" : "-warn";
        new_div.id = input['entity_type'] + div_desc;
        new_div.classList.add(input['entity_type'] + "-msg");
        let div_content = document.createTextNode(input['msg']);
        new_div.appendChild(div_content);
        input['parent'].appendChild(new_div);
        if (input['entity_type'] in ['artist, venue']) {
            input['div'].classList.add('input-warn');
        } 
    };
    if ('input-warn' in input['div'].classList) {
        input['div'].classList.remove('input-warn');
    };
}

const confirmValidTime = function(eventTarget, alt_div_id) {
    /*
    generate object for removing error messages for correctly entered errors
    */
   var data = {
    "div": eventTarget,
    "parent": eventTarget.parentElement,
    "to_exist": false,
    "entity_type": eventTarget.id,
    "success": true
   };
   if (alt_div_id) {
    data.parent = document.getElementById(alt_div_id);
   }
   toggleChildMsg(data); // remove child message
   return "none";
}

const warnInvalidTime =  function(warnKind, eventTarget) {
    /*
    {entity_type,
    div = event.target,
    parent = event.target.parentElement
    to-exist,
    success 
    */
   var data = {
    "div": eventTarget,
    "parent": eventTarget.parentElement,
    "to_exist": true,
    "entity_type": eventTarget.id,
    "success": false
   }
   switch(warnKind) {
    // invalid date warning
    case "past":
        data.msg = "Event must be scheduled for the future.";
        break;
    // invalid end date warning
    case "date-duration":
        data.msg = "End date must occur after start date";
        break;
    // invalid end end time warning
    case "negative-duration":
        data.parent = document.getElementById('time-error');
        data.msg = "End time must be after start time.";
        break;
    default:
        data.msg = "Invalid time input.";
   }
   toggleChildMsg(data);
}

const warnInvalidId = function(id, type) {
    /*
    */
    return "ID " + id + " invalid; returned no " + type;
}

const confirmValidId = function(name, type) {
    /*
    */
    return "Selected " + type + ": " + name;
}

// load blank values on form refresh
const clearDefault = function() {
    /*
    */
    let values = document.getElementsByClassName('empty-load');
    for(let i=0; i<values.length; i++) {
        values[i].value = "";
    }
    let chxs = document.getElementsByClassName('cbx');
    for(let j=0; j<chxs.length; j++) {
        chxs[j].checked = false;
    }
}

/* ----------------------------------------------------------------------
*  entity id ajax functionality
* ---------------------------------------------------------------------- */

const verifyResponse = async function(path) {
    /*
    */
    let entity_name = await fetch(path, {method: "GET", cors:"same-origin"})
        .then(function(response) {
            return response.json()
        })
        .then(function(jsonResponse) {
            var entity_value = {
                "name": false,
                "image_link": false}
            if (typeof(jsonResponse['name']) == 'string') {
                entity_value["name"] = jsonResponse['name'];
                entity_value["image_link"] = jsonResponse["img"]
            } else {entity_value = -1;}
            return entity_value;
        }
    );
    return entity_name;
}

const verifyId = async function(entity_type, event) {
    /*
    */
    let id = (event.target.value.length > 0) ? event.target.value : null;
    const path = "/" + entity_type + "s/" + id + "/verify";
    let reply = (isNaN(parseInt(id))) ? -1 : await verifyResponse(path);
    if (id===null) {reply = null;}
    let verification = {"to_exist": false,
                        "success": false,
                        "msg": "",
                        "entity_type": entity_type,
                        "div": event.target,
                        "parent": event.target.parentElement};
    switch(reply) {
        // blank input
        case null:
            verification['input_success'] = true;
            break;
        // invalid input
        case -1:
            verification['to_exist'] = true;
            verification['msg'] = warnInvalidId(id, entity_type);
            event.target.value = "";
            break;
        // valid input
        default:
            verification['to_exist'] = true;
            verification['success'] = true;
            verification['msg'] = confirmValidId(reply["name"], entity_type);
            event.target.value = id;
            if (entity_type=="artist") {
                previewArtist(reply);
            };
            if (entity_type=="venue") {
                previewVenue(reply);
            }
            console.log("VERIFIED");
            console.log(reply);
    };
    toggleChildMsg(verification);
}

/* ----------------------------------------------------------------------
*  event duration methods
* ---------------------------------------------------------------------- */
//
const verifyDuration = function(event) {
    if (eventTime.start_dt == eventTime.end_dt) {
        return "none-duration";
    } else if (eventTime.end_dt > eventTime.start_dt) {
        return true;
    } else if (eventTime.end_date > eventTime.start_date) {
        return true;
    } else if (eventTime.edd == [1970, 0, 1]) {
        if (eventTime.sdd = [1970, 0, 1]) {
            if (eventTime.end_time > eventTime.start_time) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
    else {
        return false;
    }
}

//
const setAllDayDuration = function(action) {
    /*
    * sets event value to all day
    */
    if (action == "set") {
        eventTime.stt = [0, 01];
        eventTime.ett = [23, 59];
        eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
        eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.edd);
        // document.getElementById('start_time').value = '';
        // document.getElementById('end_time').value = '';
    }
    if (action == "unset") {
        eventTime.stt = [0, 00];
        eventTime.ett = [0, 01];
        eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
        eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.edd);
        document.getElementById('start_time').value = '';
        document.getElementById('end_time').value = '';
    }
}

// calculate duration value given start_time/start_date and end_time/end_date
const calculateDuration = function() {
    if (eventTime.stt != [0, 01] && eventTime.ett [0, 01]) {
        duration_value = verifyDuration();
        if (duration_value == true) {
            var delta = (Math.abs(eventTime.end_dt - eventTime.start_dt)/60000);
            var mins = delta % 60;
            var hours = ((delta - mins)/60);
            alterDuration([hours, mins]);
        }
        else if (duration_value == "none-duration") {
            var mins = 0;
            var hours = 0;
            alterDuration(["", ""]);
        };
    };
}

// store/alter duration after its computation in DOM and global obj
const alterDuration = function(values) {
    var new_vals = (values)?values:["", ""];
    eventTime.duration.hours = new_vals[0];
    eventTime.duration.minutes = new_vals[1];
}

/* ----------------------------------------------------------------------
*  event date handling methods
* ---------------------------------------------------------------------- */
const defaultEndDate = function(event) {
    console.log("called default end date");
    if (eventTime.multi_day == false) {
        // set end date to match start date
        var data = {'type': "date_string",
        'position': "end",
        'value': event.value,
        'validation': null,
        'validated': true,
        'source': "form"};
        eventTime.set(data);
    };
    return true;
}

const validDate = function(origin) {
    /* ensure date is valid */
    console.log("called validDate()");
    var now_date = new Date();
    var valid_input;
    var msg = origin + " date validity ";
    if (origin=="start") { 
        // compare start date to current date; prevent past events
        valid_input = (eventTime.start_dt >= now_date) ? true:false;
        console.log(msg + valid_input + " after date comparison");
        if (document.getElementById('end_date').value.length > 0) { 
            // if end date exists, ensure start_date before it
            valid_input = (eventTime.end_dt >= eventTime.start_dt)?true:false;
            console.log(msg + valid_input + " after end date comparison");
        };
    }
    if (origin=="end") { 
        // compare end_date to start_date if it exists
        if (document.getElementById('start_date').value) { 
            // compare only to start_date
            valid_input = (eventTime.end_dt > eventTime.start_dt)?true:false;
            console.log(msg + valid_input + " after start date comparison");
        } else { 
            // compare only to current date
            valid_input = (eventTime.end_dt > now_date) ? true:false;
            console.log(msg + valid_input + " after date comparison");
        };
    }
    return valid_input;
}

/* ----------------------------------------------------------------------
*  event time handling methods
* ---------------------------------------------------------------------- */

/* ----------------------------------------------------------------------
*  onload listener assignments
* ---------------------------------------------------------------------- */
window.onpageshow = function() {
    // add onchange event listeners for venue and artist verification
    document.getElementById('venue_id').addEventListener('change', 
        (event) => {verifyId("venue", event);
    }, false);
    document.getElementById('artist_id').addEventListener('change', 
        (event) => {verifyId("artist", event);
    }, false);
    // add event listeners to toggle visibility of form elements
    document.getElementById('all-day').addEventListener('change', 
        (event) => {toggleTimeGroup(event)});
    document.getElementById('multi-day').addEventListener('change', 
        (event) => {toggleMultiDay(event)});
    clearDefault()
    // add time and duration listeners
    document.getElementById('start_date').addEventListener('change', 
        (event) => {acceptStart(event)});
    document.getElementById('end_date').addEventListener('change', 
        (event) => {acceptEndDate(event)});
    document.getElementById('start_time').addEventListener('change', 
        (event) => {acceptStart(event)})
    document.getElementById('end_time').addEventListener('change', 
        (event) => {acceptEndTime(event)});
}