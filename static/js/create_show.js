// declare date global
var eventTime = {
    'set_date': function(dd, tt) {
        return new Date(dd[0], dd[1], dd[2], tt[0], tt[1]);
    },
    'start': false,
    'start_time': false,
    'stt': [0, 00],
    'sdd': [1970, 1, 1],
    'start_dt': new Date(1970, 0, 1, 0, 00),
    'start_date': false,
    'end': false,
    'end_time': false,
    'ett': [0, 01],
    'edd': [1970, 1, 1],
    'end_dt': new Date(1970, 0, 1, 0, 00),
    'end_date': false,
    'all_day': false,
    'multi_day': false,
    'duration': {'hours': false,
                'minutes': false}
}
    
const verifyResponse = async function(path) {
    /*
    */
    let entity_name = await fetch(path, {method: "GET", cors:"same-origin"})
        .then(function(response) {
            return response.json()
        })
        .then(function(jsonResponse) {
            if (typeof(jsonResponse['name']) == 'string') {
                entity_value = jsonResponse['name'];
            } else {entity_value = -1;}
            return entity_value;
        })
    console.log("VALUE " + entity_name);
    return entity_name;
}

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
    //
    if (existing.length > 0) {
        for(let i = 0; i < existing.length; i++) {
            existing[i].remove();
        }
    }
    //
    if (input['to_exist']==true) {
        let new_div = document.createElement('div');
        let div_desc = (input['success'] == true) ? "-confirm" : "-warn";
        new_div.id = input['entity_type'] + div_desc;
        new_div.classList.add(input['entity_type'] + "-msg");
        console.log(new_div);
        let div_content = document.createTextNode(input['msg']);
        new_div.appendChild(div_content);
        input['parent'].appendChild(new_div);
    }
}

const confirmValidId = function(name, type) {
    /*
    */
    return "Selected " + type + ": " + name;
}

const acceptStart = function(event) {
    var type = event.target.id;
    var val = event.target.value;
    if (type == 'start_time') {
        eventTime.stt = val.split(':');
        if (setEndTime("start")==true) {
            // if duration + || undefined, set start_time
            eventTime.start_time = val; 
            console.log("confirm start_time value");
        } else {
            // if duration invalid, reset start temps to default
            eventTime.stt = [0, 1];
            eventTime.start_dt = eventTime.set_date(eventTime.sdd,
                                                        eventTime.stt);
            console.log("reject start_time value");
        };
    }
    else if (type == 'start_date') {
        start_date = val.split('-');
        start_date[1] -= 1;
        eventTime.sdd = start_date;
        // confirm start date is in the future
        if (validDate("start") != false) {
            eventTime.start_date = start_date.join('-');
            defaultEndDate("set");
            confirmValidTime(event.target);
            console.log("confirm start_time value");
        }
        else {
            eventTime.start_date = "1970-0-1";
            eventTime.sdd = [1970, 0, 1];
            event.target.value = '';
            defaultEndDate("unset");
            warnInvalidTime("past", event.target);
            console.log("reject start_date value");
        };
    };
    if (eventTime.start_date!=false && eventTime.start_time!=false) {
        eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
    }
    console.log(eventTime);
};

const confirmValidTime = function(eventTarget) {
    /*
    */
   var data = {
    "div": eventTarget,
    "parent": eventTarget.parentElement,
    "to_exist": false,
    "entity_type": eventTarget.id,
    "success": true
   }
   toggleChildMsg(data);
   return "none";
}

const warnInvalidId = function(id, type) {
    /*
    */
    return "ID " + id + " invalid; returned no " + type;
}

const warnInvalidTime =  function(warnKind, eventTarget) {
    /*
    */
   console.log("called warnInvalidTime")
   var data = {
    "div": eventTarget,
    "parent": eventTarget.parentElement,
    "to_exist": true,
    "entity_type": eventTarget.id,
    "success": false
   }
   switch(warnKind) {
    case "past":
        data.msg = "Event must be scheduled for the future.";
        break;
    case "negative-duration":
        data.msg = "End time must be after start time.";
        break;
    default:
        data.msg = "Invalid time input.";
   }
   console.log(data);
   toggleChildMsg(data);
}

const verifyId = async function(entity_type, event) {
    /*
    */
    let id = (event.target.value.length > 0) ? event.target.value : null;
    let reply = (isNaN(parseInt(id))) ? -1 : await verifyResponse("/" + entity_type + "s/" + id + "/verify");
    if (id===null) {reply = null;}
    let verification = {"to_exist": false,
                        "success": false,
                        "msg": "",
                        "entity_type": entity_type,
                        "parent": event.target.parentElement}
    switch(reply) {
        case null:
            console.log("blank input");
            verification['input_success'] = true;
            break;
        case -1:
            console.log("invalid input");
            verification['to_exist'] = true;
            verification['msg'] = warnInvalidId(id, entity_type);
            event.target.value = "";
            break;
        default:
            console.log("valid input");
            verification['to_exist'] = true;
            verification['input_success'] = true;
            verification['msg'] = confirmValidId(reply, entity_type)
    };
    console.log("input_msg is now " + verification['msg'])
    /*
    */
    toggleChildMsg(verification);    
}

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

const verifyDuration = function(event) {
    return "none";
}

const setDuration = function(event) {
    /*
    * accepts or programatically creates end time
    *   - if duration has a valid value, accepts it and calls
    *      setEndTime to change end time
    *   - called when setEndTime has a valid value
    */
    console.log("called SetDuration");
}

const calculateDuration = function() {
    console.log("called calculate duration");
    var delta = (Math.abs(eventTime.end_dt - eventTime.start_dt)/60000);
    var mins = delta % 60;
    var hours = (delta - mins) / 60;
    alterDuration([hours, mins]);
}

const alterDuration = function(values) {
    var new_vals = (values)?values:["", ""];
    document.getElementById('hours').value = new_vals[0];
    eventTime.duration.hours = new_vals[0];
    document.getElementById('mins').value = new_vals[1];
    eventTime.duration.minutes = new_vals[1];
}

const defaultEndDate = function(action) {
    console.log("using default end date to " + action + " date")
    if (eventTime.multi_day == false) {
        // set end date to match start date
        if (action=='set') {
            eventTime.end_date = eventTime.start_date;
            eventTime.edd = eventTime.start_date.split("-");
            eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.sdd);
        }
        // clear all times
        // set start and end to false and temps to defaults
        else if (action=="unset") {
            eventTime.start_date = false;
            eventTime.sdd = [1970, 0, 1];
            eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
            eventTime.end_date = false;
            eventTime.edd = [1970, 0, 1];
            eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.sdd);
        }
    }
}

const validDate = function(origin) {
    var now_date = new Date();
    var valid_input;
    if (origin=="start") {
        eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
        valid_input = (eventTime.start_dt >= now_date) ? true:false;
        console.log("start date validity compared to current date");
        if (eventTime.end_date) {
            valid_input = (eventTime.end_dt >= eventTime.start_dt)?true:false;
            console.log("  -> validity compared to end_dt");
        }
    }
    if (origin=="end") {
        eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.ett);
        if (eventTime.start_date) {
            valid_input = (event_time.end_dt >= event_time.start_dt)?true:false;
            console.log("end date validty compared to existing start date");
        } else {
            valid_input = (eventTime.start_dt >= now_date) ? true:false;
            console.log("end date validty compared to current date");
        }
    }
    console.log("validDate(" + origin + ") found new value " + valid_input);
    return valid_input;
}

const verifyEndTime = function(event) {
    var val = event.target.value;
    eventTime.ett = val.split(':');
    is_valid = setEndTime(); // !! add event end time to global object
    if (is_valid==true) {
        console.log("valid duration");
        eventTime.end_time = val;
        confirmValidTime(event.target);
    } else if (is_valid==false) {
        console.log("invalid duration");
        warnInvalidTime("negative-duration", event.target);
        alterDuration();
    }
    console.log("-------------------------------------.");
    console.log(eventTime);
    console.log("-------------------------------------.");
    return "none";
}

const setEndTime = function(origin) {
    /*
    * accepts or programmatically creates end time
    *   - if endtime has a valid value, accepts it and calls
    *      setDuration to change end time
    *   - called when setDuration has a valid value
    */
    console.log("called setEndTime ");
    var alteredStart = false;
    var hasStart = (origin=="end" && eventTime.start_time != false)?true:false;
    var hasEnd = (origin=="start" && eventTime.end_time != false)?true:false;
    console.log("has start? " + hasStart);
    console.log("has end? " + hasEnd);
    /* if end_date has been set but start_date hasn't, set start_date temp values
       equal to end_date values */ 
    if (eventTime.start_date == false && eventTime.end_date != false) {
        eventTime.sdd = eventTime.edd;
        alteredStart = true;
        console.log("   > set start_date special case");
    }
    /* verify Datetime objects have been created for both start and end
       temporary objects */
    eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
    eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.ett);
    // compare dates
    var is_valid = (eventTime.end_dt >= eventTime.start_dt)?true:false;
    console.log("INNER DURATION IS " + is_valid);
    if (is_valid == true) { // set global values for time and duration
        calculateDuration();
        if (origin=="start") {
            eventTime.start_time == eventTime.stt.join(":");
        }
        if (origin=="end") {
            eventTime.end_time == eventTime.ett.join(":");
        }
        console.log(origin + " value accepted, set global");
    } else {
        console.log(origin + "value rejected.");
        if (origin=="start") {
            if (hasEnd == true) { // reset start temps and prep for invalid return
                eventTime.stt = [0, 00];
                if (alteredStart == true) {
                    eventTime.sdd = [1970, 0 , 1];
                }
                eventTime.start_dt = eventTime.set_date(eventTime.sdd, eventTime.stt);
                console.log('confirmed inalid duration. see global @ assessment: ')
                console.log(eventTime);
            } else { // return valid update
                eventTime.start_time == eventTime.stt.join(":");
                is_valid = true;
                console.log("   - reset b/c missing end. valid input det.");
            }
        }
        if (origin=="end") { 
            if (hasStart == false) { // reset end temps and prep for invalid return
                eventTime.edd = [0, 00]
                eventTime.end_dt = eventTime.set_date(eventTime.edd, eventTime.ett);
                console.log('confirmed inalid duration. see global @ assessment: ')
                console.log(eventTime);
            } else { // return valid update
                eventTime.end_time = eventTime.ett.join(":");
                is_valid = true
                console.log("    - reset b/c missing start. valid input det.")
            }
        }
    }
    return is_valid;
}

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
        console.log("true -- checked");
        toggleHiddenClass("time-group", false);
    }
    else {
        console.log("false -- unchecked");
        toggleHiddenClass("time-group", true);
    }
}

const toggleMultiDay = function(event) {
    /*
    * checkbox listener; shows or hides end data inputs
    */
    if (event.target.checked) {
        console.log("true -- checked");
        toggleHiddenClass("end-date-group", true);
    }
    else {
        console.log("false -- unchecked");
        toggleHiddenClass("end-date-group", false);
    }
}

window.onpageshow = function() {
    // add onchange event listeners for venue and artist verification
    document.getElementById('venue_id').addEventListener('change', (event) => {
        verifyId("venue", event);
    }, false);
    document.getElementById('artist_id').addEventListener('change', (event) => {
        verifyId("artist", event)
    }, false);
    // add event listeners to toggle visibility of form elements
    document.getElementById('all-day').addEventListener('change', (event) => {toggleTimeGroup(event)});
    document.getElementById('multi-day').addEventListener('change', (event) => {toggleMultiDay(event)});
    clearDefault()
    // add time and duration listeners
    document.getElementById('start_date').addEventListener('change', (event) => {acceptStart(event)});
    document.getElementById('start_time').addEventListener('change', (event) => {acceptStart(event)})
    document.getElementById('end_time').addEventListener('change', (event) => {verifyEndTime(event)});
}