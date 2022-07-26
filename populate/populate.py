"""
includes classes designed to automate creation of randomized attributes
for Venue, Artist, and Show entities in fyyur database
"""
import random
from sys import exc_info as sysinfo
import datetime
from calendar import monthrange
from pprint import pprint
import psycopg2

# import & config python built-in logging library
import logging
logging.basicConfig(filename='poplog.log', level=logging.DEBUG)

#  ----------------------------------------------------------------------------
# / random data generation
# -----------------------------------------------------------------------------

class RdDb:
    """
    Contains lists & dictionaries of default data and functions to return random
    data to Venue and Artist entities
    """
    # pylint: disable=line-too-long
    # no human needs to read this url data. seriously, just close this part.
    default_images = {
        'venue': {'search': "https://images.unsplash.com/photo-1573339887617-d674bc961c31?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1534&q=80"
            }
    }
    genre_list = ["Alternative", "Blues", "Classical", "Country", "Electronic", 
                    "Folk", "Funk", "Hip-Hop", "Heavy Metal", "Instrumental", 
                    "Jazz", "Musical Theatre", "Pop", "Punk", "R&B", "Reggae",
                    "Rock n Roll", "Soul", "Other"]
    location_names = ['San Francisco', 'New York', 'Los Angeles', 'New Orleans',
        'Nashville', 'Chicago', 'Austin', 'Philadelphia', 'Atlanta']
    locations = {
        'San Francisco' : {
            'artist_ids': [],
            'venue_ids': [],
            'state' : "CA",
            'area_codes' : [415, 628],
            'zip_codes': [94109, 94110, 94122, 94112,
                94115, 94102, 94117, 94121, 94103,
                94118, 94107, 94114, 94116, 94123,
                94131, 94133, 94134, 94124, 94132,
                94105, 94127, 94108, 94158, 94111,
                94129, 94119, 94188, 94142, 94141,
                94130, 94140, 94147, 94164, 94159,
                94104, 94146, 94126, 94016, 94172,
                94125, 94120, 94143, 94144, 94145,
                94136, 94137, 94150, 94151, 94152,
                94153, 94154, 94155, 94156, 94157,
                94138, 94139, 94160, 94161, 94162,
                94163, 94101, 94165, 94166, 94167,
                94168, 94169, 94170, 94171, 94106,
                94175, 94177, 94135, 94199]},
        'New York' : {
            'artist_ids': [],
            'venue_ids': [],
            'state' : "NY",
            'area_codes': [300, 914, 718, 212],
            'zip_codes': [10025, 10023, 10002, 10016,
                10029, 10009, 10011, 10128, 10019,
                10003, 10463, 10024, 10028, 10027,
                10021, 10032, 10031, 10451, 10014,
                10036, 10033, 10010, 10022, 10065,
                10001, 10040, 10034, 10026, 10013,
                10035, 10075, 10012, 10454, 10038,
                10030, 10017, 10039, 10037, 10018,
                10005, 10044, 10280, 10069, 10007,
                10282, 10006, 10004, 10116, 10163,
                10150, 10162, 10008, 10276, 10101,
                10159, 10108, 10113, 10185, 10272,
                10156, 10274, 10129, 10268, 10102,
                10103, 10104, 10105, 10106, 10107,
                10043, 10109, 10110, 10111, 10112,
                10015, 10114, 10115, 10045, 10117,
                10118, 10119, 10120, 10121, 10122,
                10123, 10124, 10125, 10126, 10046,
                10047, 10130, 10131, 10132, 10133,
                10138, 10149, 10048, 10151, 10152,
                10153, 10154, 10155, 10055, 10157,
                10158, 10060, 10160, 10161, 10020,
                10072, 10164, 10165, 10166, 10167,
                10168, 10169, 10170, 10171, 10172,
                10173, 10174, 10175, 10176, 10177,
                10178, 10179, 10184, 10079, 10196,
                10197, 10199, 10203, 10211, 10212,
                10213, 10242, 10249, 10256, 10257,
                10258, 10259, 10260, 10261, 10265,
                10080, 10269, 10270, 10271, 10081,
                10273, 10082, 10275, 10087, 10277,
                10278, 10279, 10090, 10281, 10094,
                10285, 10286, 10292, 10095, 10096,
                10098, 10099, 10041]},
        'Los Angeles' : {
            'artist_ids': [],
            'venue_ids': [],
            'state': "CA",
            'area_codes': [213, 310, 424, 661, 818, 323],
            'zip_codes': [90250, 90046, 90034, 90805, 90650,
                90044, 90026, 90066, 90019, 90004,
                90280, 91342, 90201, 90706, 90025,
                90011, 90027, 91335, 90731, 93536,
                93550, 93535, 90802, 90631, 90036,
                90640, 91331, 91801, 90042, 90028,
                90006, 90255, 90024, 91402, 91367,
                91766, 91406, 90049, 91706, 90277,
                90020, 91744, 91601, 91405, 90813,
                90005, 90803, 91702, 90503, 91343,
                90043, 91770, 90047, 90003, 90247,
                90045, 90016, 90037, 91304, 90018,
                93551, 90022, 91344, 90278, 90703,
                90057, 91745, 90660, 91765, 91605,
                90275, 90745, 91016, 90804, 90815,
                90065, 93534, 91606, 90292, 90029,
                90291, 91732, 91423, 90501, 90262,
                90723, 90069, 92821, 90241, 90405,
                91401, 91767, 90638, 90008, 90266,
                91205, 91387, 90505, 91604, 90403,
                90808, 90744, 90017, 91306, 91748,
                90012, 91311, 90035, 91607, 90007,
                90048, 91350, 91505, 91750, 90015,
                91107, 90032, 90068, 91206, 90001,
                90807, 91326, 90063, 90064, 90033]
            },
        'Nashville': {
            'artist_ids': [],
            'venue_ids': [],
            'state': "TN",
            'area_codes': [423, 615, 629, 731, 865, 901, 931],
            'zip_codes': [37013, 37211, 37027, 37209, 37221,
                37076, 37115, 37207, 37214, 37203,
                37217, 37206, 37072, 37086, 37205,
                37215, 37208, 37138, 37216, 37212,
                37210, 37204, 37218, 37080, 37220,
                37219, 37143, 37189, 37228, 37201,
                37024, 37011, 37070, 37229, 37116,
                37222, 37202, 37224, 37213, 37227,
                37230, 37232, 37234, 37235, 37236,
                37237, 37238, 37240, 37241, 37242,
                37243, 37244, 37245, 37246, 37247,
                37248, 37249, 37250]
            },
        'New Orleans': {
            'artist_ids': [],
            'venue_ids': [],
            'state': "LA",
            'area_codes': [504],
            'zip_codes':[70119, 70115, 70118, 70117, 70122,
                70126, 70130, 70131, 70114, 70124,
                70127, 70116, 70125, 70128, 70113,
                70112, 70129, 70187, 70174, 70179,
                70175, 70182, 70185, 70177, 70158,
                70156, 70186, 70157, 70184, 70152]
            },
        'Chicago': {
            'artist_ids': [],
            'venue_ids': [],
            'state': "IL",
            'area_codes': [312, 773],
            'zip_codes': [60657, 60614, 60640, 60647, 60618,
                60613, 60610, 60625, 60629, 60611,
                60619, 60617, 60620, 60634, 60016,
                60628, 60626, 60649, 60622, 60616,
                60615, 60641, 60660, 60453]
            },
        'Austin': {
            'artist_ids': [],
            'venue_ids': [],
            'state': "TX",
            'area_codes': [512],
            'zip_codes': [77474, 77418, 78950, 78933, 78944,
                78931, 77473, 77452]
            },
        'Philadelphia': {
            'artist_ids': [],
            'venue_ids': [],
            'state': "PA",
            'area_codes': [267, 215, 445],
            'zip_codes': [19143, 19111, 19124, 19104, 19120,
                19134, 19148, 19131, 19144, 19146,
                19145, 19140, 19147, 19149, 19103,
                19139, 19121, 19128, 19130, 19132,
                19115, 19114, 19152]
            },
        'Atlanta': {
            'artist_ids': [],
            'venue_ids': [],
            'state': "GA",
            'area_codes': [404, 470, 678, 770],
            'zip_codes': [30349, 30318, 30331, 30004, 30022,
                30075, 30319, 30328, 30309, 30324,
                30097, 30339, 30076, 30350, 30305,
                30213, 30316, 30311, 30344, 30342,
                30308, 30312, 30005, 30315, 30310,
                30306]
            }
        }
    names = { 'street_names': [ "Second", "Third", "First", "Fourth", "Park",
                "Fifth", "Main", "Sixth", "Oak", "Seventh", "Pine", "Maple",
                "Cedar", "Eighth", "Elm", "View", "Washington", "Ninth",
                "Lake", "Hill", "Lee", "Dogwood", "Magnolia", "Aspen",
                "Church", "School", "Hemlock", "Jackson", "Mulberry", "Broad",
                "King", "Ridge", "Cherry"],
              'street_ends': ['Road', "Street", "Lane", "Blvd", "Ave"],
              'first_names': [ "Michael", "Christopher", "Jessica", "Matthew",
                "Ashley", "Jennifer", "Joshua", "Amanda", "Daniel", "David",
                "James", "Robert", "John", "Joseph", "Andrew", "Ryan",
                "Brandon", "Jason", "Justin", "Sarah", "William", "Jonathan",
                "Stephanie", "Brian", "Nicole", "Nicholas", "Anthony",
                "Heather", "Eric", "Elizabeth", "Adam", "Megan", "Melissa",
                "Kevin", "Steven", "Thomas", "Timothy", "Christina", "Kyle",
                "Rachel", "Laura", "Lauren", "Amber", "Brittany", "Danielle",
                "Richard", "Kimberly", "Jeffrey", "Amy", "Crystal", "Michelle",
                "Tiffany", "Jeremy", "Benjamin", "Mark", "Emily", "Aaron",
                "Charles", "Rebecca", "Jacob", "Stephen", "Patrick", "Sean",
                "Erin", "Zachary", "Jamie", "Kelly", "Samantha", "Nathan",
                "Sara", "Dustin", "Paul", "Angela", "Tyler", "Scott",
                "Katherine", "Andrea", "Gregory", "Erica", "Mary", "Travis",
                "Lisa", "Kenneth", "Bryan", "Lindsey", "Kristen", "Jose",
                "Alexander", "Jesse", "Katie", "Lindsay", "Shannon", "Vanessa",
                "Courtney", "Christine", "Alicia", "Cody", "Allison", "Bradley",
                "Samuel", "Shawn", "April", "Derek", "Kathryn", "Kristin",
                "Chad", "Jenna", "Tara", "Maria", "Krystal", "Jared", "Anna",
                "Edward", "Julie", "Peter", "Holly", "Marcus", "Kristina",
                "Natalie", "Jordan", "Victoria", "Jacqueline", "Corey",
                "Keith", "Monica", "Juan", "Donald", "Cassandra", "Meghan",
                "Joel", "Shane", "Phillip", "Patricia", "Brett", "Ronald",
                "Catherine", "George", "Antonio", "Cynthia", "Stacy",
                "Kathleen", "Raymond", "Carlos", "Brandi", "Douglas",
                "Nathaniel", "Ian", "Craig", "Brandy", "Alex", "Valerie",
                "Veronica", "Cory", "Whitney", "Gary", "Derrick", "Philip",
                "Luis", "Diana", "Chelsea", "Leslie", "Caitlin", "Leah",
                "Natasha", "Erika", "Casey", "Latoya", "Erik", "Dana",
                "Victor", "Brent", "Dominique", "Frank", "Brittney", "Evan",
                "Gabriel", "Julia", "Candice", "Karen", "Melanie", "Adrian",
                "Stacey", "Margaret", "Sheena", "Wesley", "Vincent",
                "Alexandra", "Katrina", "Bethany", "Nichole", "Larry",
                "Jeffery", "Curtis", "Carrie", "Todd", "Blake", "Christian",
                "Randy", "Dennis", "Alison", "Trevor", "Seth", "Kara", "Joanna",
                "Rachael", "Luke", "Felicia", "Brooke", "Austin", "Candace",
                "Jasmine", "Jesus", "Alan", "Susan", "Sandra", "Tracy", "Kayla",
                "Nancy", "Tina", "Krystle", "Russell", "Jeremiah", "Carl",
                "Miguel", "Tony", "Alexis", "Gina", "Jillian", "Pamela",
                "Mitchell", "Hannah", "Renee", "Denise", "Molly", "Jerry",
                "Misty", "Mario", "Johnathan", "Jaclyn", "Brenda", "Terry",
                "Lacey", "Shaun", "Devin", "Heidi", "Troy", "Lucas", "Desiree",
                "Jorge", "Andre", "Morgan", "Drew", "Sabrina", "Miranda",
                "Alyssa", "Alisha", "Teresa", "Johnny", "Meagan", "Allen",
                "Krista", "Marc", "Tabitha", "Lance", "Ricardo", "Martin",
                "Chase", "Theresa", "Melinda", "Monique", "Tanya", "Linda",
                "Kristopher", "Bobby", "Caleb", "Ashlee", "Kelli", "Henry",
                "Garrett", "Mallory", "Jill", "Jonathon", "Kristy", "Anne",
                "Francisco", "Danny", "Robin", "Lee", "Tamara", "Manuel",
                "Meredith", "Colleen", "Lawrence", "Christy", "Ricky", "Jay",
                "Randall", "Marissa", "Ross", "Mathew", "Jimmy", "Abigail",
                "Kendra", "Carolyn", "Billy", "Deanna", "Jenny", "Jon",
                "Albert", "Taylor", "Lori", "Rebekah", "Cameron", "Ebony",
                "Wendy", "Angel", "Micheal", "Kristi", "Caroline", "Colin",
                "Dawn", "Kari", "Clayton", "Arthur", "Roger", "Roberto",
                "Priscilla", "Darren", "Kelsey", "Clinton", "Walter", "Louis",
                "Barbara", "Isaac", "Cassie", "Grant", "Cristina", "Tonya",
                "Rodney", "Bridget", "Joe", "Cindy", "Oscar", "Willie",
                "Maurice", "Jaime", "Angelica", "Sharon", "Julian", "Jack"],
              'last_names': ["Smith", "Johnson", "Williams", "Brown", "Jones",
                "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee",
                "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
                "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen",
                "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera",
                "Campbell", "Mitchell", "Carter"],
              'nicknames': ["Leo", "Fitz", "Sadie", "Billie", "Ray", "Teddy",
                "Ace", "Scotty", "Rusty", "Mac", "Bo", "Cal"],
              'band_names': {
                's_word': ["Salutations", "Intrepid", "Vermillion",
                    "The Blueberries", "Mirrormen", "Inspired", "Veryfied",
                    "Repercussions", "Pinteresse", "CRUD", "Orega-no-no-no",
                    "SmartFella"],
                'multi_word': {
                    'first_word': ["The", "Many", "Three", "Little", "Tiny",
                        "Grand", "Ferocious", "Wild", "Crazed", "Simple",
                        "Loud", "Bitter", "Killer", "Cold", "From", "Also",
                        "Argubally", "Lively", "Noted", "Famous"],
                    'second_word': ["Sweet", "Crowded", "Frosted", "Little",
                        "New", "Cherry", "Lousy", "Cyber", "Buzzing", "Wicked",
                        "Insane", "Simple", "Flat", "Soul", "Paper", "Front",
                        "Past", "Acid", "Sharp", "Righteous", "Grateful",
                        "Untimely", "Bespoke", "Rickety", "Mauve", "Classical",
                        "Trusted", "Trust", "Cranberry"],
                    'third_word': ["Crowds", "Parks", "Tips", "Lanes", "Grids",
                        "Palor", "Belles", "Valor", "Loss", "Chaos", "Tantrums",
                        "Fellas", "Fury", "Juice", "Cowboys", "Hens", "Pieces",
                        "Berries", "Wheels", "Will", "Stars", "Rockets",
                        "Sheep", "Flock", "Freshies", "Lashes", "Turn",
                        "Denouement", "Pictures", "Lights", "Engineers",
                        "Developers"]}},
              'venue_types': ["Gallery", "Hall", "Lounge", "Bar",
                "Bar & Lounge", "Theater", "Parlor", "Room"]}
    artist_images = ["https://images.unsplash.com/photo-1521337581100-8ca9a73a5f79?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1570&q=80",
        "https://images.unsplash.com/photo-1545266086-d245dccef238?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80",
        "https://images.unsplash.com/photo-1544219548-0cbb0eebc84b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80",
        "https://images.unsplash.com/photo-1598517834429-cf49a9e6077d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1532&q=80",
        "https://images.unsplash.com/photo-1619378879648-2a5aa45eecad?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80",
        "https://images.unsplash.com/photo-1515210986222-9a86ccb8f4a9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1508&q=80",
        "https://images.unsplash.com/photo-1520224327482-f7863d2c3865?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80",
        "https://images.unsplash.com/photo-1518501257902-61d237c71f21?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1500&q=80",
        "https://images.unsplash.com/photo-1542813813-e6546b5d4914?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1500&q=80",
        "https://images.unsplash.com/photo-1578873375841-468b1557216f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1534&q=80",
        "https://images.unsplash.com/photo-1598519502953-96e1fb8d4a09?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1601&q=80",
        "https://images.unsplash.com/photo-1511854085838-e8808da760f5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1592&q=80",
        "https://images.unsplash.com/photo-1520170975578-25bd5217bf3d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1500&q=80"]
    venue_images = ["https://images.unsplash.com/photo-1558620013-a08999547a36?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1489&q=80",
        "https://images.unsplash.com/photo-1565798846807-2af22c843402?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1516&q=80",
        "https://images.unsplash.com/photo-1576514129883-2f1d47a65da6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1567&q=80",
        "https://images.unsplash.com/photo-1534353341328-aede12f06b84?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1582&q=80",
        "https://images.unsplash.com/photo-1470229538611-16ba8c7ffbd7?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80"]

    @staticmethod
    def new_band_word(word_list):
        """
        returns word or words from name dict
        accepts a list of integers as an input and returns list of the same
        length filled with appropriate random choices
        """
        words = []
        band_words = RdDb.names["band_names"]["multi_word"]
        for i in word_list:
            if i==1:
                word = random.choice(band_words["first_word"])
            if i==2:
                word = random.choice(band_words["second_word"])
            if i==3:
                word = random.choice(band_words["third_word"])
            if i==0:
                word = random.choice(RdDb.names["band_names"]["s_word"])
            words.append(word)
        logging.debug("RdDb.new_band_word returning " + str(words))
        logging.info("RdDb.new_band_word completed")
        return words

    @staticmethod
    def new_location(location_name):
        """
        return dictionary of location information
        accepts one parameter:
         - location name: either a name of a city that is also a key in the 
            RdDb.location_names or -1 if one is not specified
        returns an object containing city, area_code, state and zip_code
        """
        if location_name in RdDb.location_names or location_name == -1:
            if location_name == -1:
                city = random.choice(RdDb.location_names)
            if location_name in RdDb.location_names:
                city = location_name
            loc_dict = RdDb.locations[city]
            location = {"city": city,
                        "area_code": random.choice(loc_dict["area_codes"]),
                        "state": loc_dict["state"], 
                        "zip_code": random.choice(loc_dict["zip_codes"])}
        else:
            location = None
        return location
        logging.info("RdDb.new_location completed")

    @staticmethod
    def new_phone(area_code):
        """
        returns phone number formatted as a string
        """
        phone = "(" + str(area_code) + ")"
        phone = phone + str(random.choice(range(101, 999))) + "-"
        phone = phone + str(random.choice(range(1000, 9999)))
        logging.debug("RdDb.new_phone returning " + str(phone))
        logging.info("RdDb.new_phone completed")
        return phone

    @staticmethod
    def new_address():
        """
        generates random specific street address
        """
        street = random.choice(RdDb.names["street_names"])
        street_end = random.choice(RdDb.names["street_ends"])
        full_street = street + " " + street_end
        address = str(random.choice(range(100, 9999))) + " "
        address = address + full_street
        address_dict = { "short_street" : street,
                            "street" : full_street,
                            "address" : address}
        logging.debug("RdDb.new_address returning " + str())
        logging.info("RdDb.new_address completed")
        return address_dict

    @staticmethod
    def new_genres():
        """
        return a list of genres. Genres and list length are random.
        """
        genres = RdDb.genre_list
        llen = random.choice(range(1,7))
        i = 0
        genre_list = []
        genre_string = ""
        while i < llen:
            genre_name = random.choice(genres)
            if genre_name not in genre_list:
                genre_list.append(genre_name)
            i += 1
        logging.debug("RdDb.new_genres returning " + str(genre_list))
        logging.info("RdDb.new_genres completed")
        return genre_list

    @staticmethod
    def new_person_name():
        """
        returns random first & last name pair as tuple to be used by
        generate_name methods in Artist and Venue entities
        """
        first_name = random.choice(RdDb.names["first_names"])
        last_name = random.choice(RdDb.names["last_names"])
        logging.info("RdDb.new_person_name completed")
        return (first_name, last_name)

    @staticmethod
    def new_venue_type():
        """
        returns random venue type to be used by generate_name methods to be
        used by generate_name methods in Artist and Venue entities
        """
        random_venue = random.choice(RdDb.names["venue_types"])
        logging.debug("RdDb.new_venue_type returning " + str(random_venue))
        logging.info("RdDb.new_venue_type completed")
        return random_venue

    @staticmethod
    def uris(name):
        """
        return uris generated from name as tuple for website_link and
        facebook_link attributes in Artist and Venue entities
        """
        logging.info("called RdDb.")
        name = name.replace("'", "")
        name = name.replace(" ", "")
        name = name.lower()
        facebook_link = "www.facebook.com/" + name
        website_link = "www." + name + ".com"
        logging.info("RdDb.uris completed")
        return (facebook_link, website_link)

    @staticmethod
    def new_schedule_item():
        """
        selects a random date incl starting time and end time
          based on a randomly selected show duration
        returns a tuple containing two datetimes
        """
        nowobj = datetime.datetime.now()
        future_date = random.choice([False, True, True])
        if future_date:
            future_year = nowobj.year + 10
            year = random.choice(range(nowobj.year, future_year))
            month = random.choice(range(1, 13))
        else:
            past_year = nowobj.year - 5
            year = random.choice(range(past_year, nowobj.year))
            month = random.choice(range(1, nowobj.month + 1))
            if month == nowobj.month and year == nowobj.year:
                date = random.choice(range(1, nowobj.month))
        day = random.choice(range(1, monthrange(year, month)[1] + 1))
        hour = random.choice(range(12, 22))
        minutes = random.choice([0, 15, 30])
        start_date = datetime.datetime(year, month, day, hour, minutes)
        hours = random.choice(range(1, 4))
        minutes = random.choice([0, 15, 30])
        end_date = start_date + datetime.timedelta(hours=hours, minutes=minutes)
        return (start_date, end_date)

#  ----------------------------------------------------------------------------
# / Temporary (global) model generation and modification
# -----------------------------------------------------------------------------

class ThinData:

    def __init__(self):
        """
        init instance of RdDb item
        """
        self.log("call", "__init__")
        self.locs = {}
        self.log_global = 0
        self.genre_ids = []
        self.genres = {}
        self.artist_ids = []
        self.venue_ids = []
        self.show_ids = []
        self.model = self.blank_singleton()
        logging.info("completed RdDb __init__")

    def log(self, log_type, ftn_name, **kwargs):
        """
        forms a string to log a message for ThinData function
        """
        info_msg = "Thindata." + ftn_name
        if log_type == "call":
            info_msg = "called " + info_msg
        if log_type == "out":
            info_msg += "completed."
            debug_msg = ""
            if ftn_name == "append_existing":
                debug_msg += "Returning new model"
            if "add" in kwargs.keys():
                 debug_msg += "\nAdded " + kwargs["add"]  
            if "find" in kwargs.keys():
                 debug_msg += "\nFound " + kwargs["find"]
            if "entity_string" in kwargs.keys():
                 debug_msg += "\nUpdated model to include "
                 debug_msg += kwargs["entity_string"] 
            logging.debug(debug_msg)
        if log_type == "err":
            err_msg = info_msg + " failed with error code "
            err_msg += str(kwargs["error_code"])
        logging.info(info_msg)

    def blank_singleton(self):
        """
        creates a blank, standardized object for each location in 
            RdDb.location names and adds it to and self.locs[<location>]
        returns the updated model
        """
        model = {"artists": [],
                    "shows": [],
                    "venues": []}
        for loc in RdDb.location_names:
            obj = {"venues": {},
                            "venue_ids": [],
                            "artists": {},
                            "artist_ids": [],
                            "shows": {"ids": []}}
            model[loc] = obj
            self.locs[loc] = obj
        return model

    def append_existing(self):
        """
        get all venue and artist ids by location and add them to both:
            - self.locations[location]["venue_ids"] and
                self.locations[location]["artist_ids"]
                (contains only ids for location)
            - self.artist_ids and self.venue_ids (contains all ids)
        """
        def log_singleton(function, *args):
            """
            creates logging messages for the log_singleton() function
            """
            if function == "call":
                msg = "called RdDb.append_existing()"
                logging.info(msg)
            if function == "summarize" and len(args) == 3:
                data_function = "self.venue_ids is " + str(args[1])
                data_function += "\n  & self.artist_ids is " + str(args[2])
                logging.debug(data_function)
                msg = "Rd.Db.append_existing completed"
                logging.info(msg)

        log_singleton("call")
        for location in RdDb.location_names:
            self.locs[location] = {"venues": {},
                                    "venue_ids": [],
                                    "artists": {},
                                    "artist_ids": [],
                                    "shows": {"ids": []}}
            ids = Select().loc_search(location)
            # add venue info to location
            for item in ids[0]:
                self.append_venue(True, location, item)
            # add artist info to location
            for item in ids[1]:
                self.append_artist(True, location, item)
            # add show details to location
            for item in self.locs[location]["shows"]["ids"]:
                self.append_show(True, location, item)
            self.locs[location] = self.model[location]
        self.model["artists"] = self.artist_ids
        self.model["venues"] = self.venue_ids
        self.model["shows"] = self.show_ids
        self.model["genres"] = {}
        log_singleton("summarize", self.venue_ids, self.artist_ids)
        return self.model

    def __repr__(self):
        """
        represent data in RdDb class instance
        """
        msg = "\n" + "-" * 30 + "\n" + str(pprint(self.model))
        msg += "(global) RdDb (random data) item: "
        msg += "\n   - artist_ids: " + str(self.artist_ids) 
        msg += "\n   - venue_ids: " + str(self.venue_ids)
        msg += "\n   - show_ids: " + str(self.show_ids)
        msg += "\n   - genre_ids: " + str(self.genre_ids)
        msg += "\n" + "-" * 30 + "\n"
        return msg

    def self_populate(self, retain_blank):
        """
        finds existing records for artist, venue and show ids and
          adds their IDs to the global model
        """
        if retain_blank == False:
            self.artist_ids = Select().get_entity_ids("artist")
            self.venue_ids = Select().get_entity_ids("venue")
            self.show_ids = Select().get_entity_ids("show")
            self.model = self.append_existing()

    def append_venue(self, extant, loc, v_id):
        """
        add venue id (v_id) to global object
        """
        obj = {"type": "venue",
                "loc": loc,
                "extant": extant,
                "id": v_id}
        control = self.append_global_id(obj)
        if control == True:
            control = self.append_local_id(obj)
        if control == True:
            control = self.append_local_id_object(obj)
        if control == True and extant==True: 
            control = self.append_show_id_lists(obj)
        return control

    def append_artist(self, extant, loc, a_id):
        """
        add artist id (a_id) to global object
        """
        obj = {"type": "artist",
                "loc": loc,
                "extant": extant, 
                "id": a_id}
        control = self.append_global_id(obj)
        if control == True:
            control = self.append_local_id(obj)
        if control == True:
            control = self.append_local_id_object(obj)
        if control == True and extant==True:
            control = self.append_show_id_lists(obj)
        return control

    def append_global_id(self, obj):
        """
        add entity id (obj input variable) to appropriate global locations
        in the global object
        """
        success = False
        if obj["type"] == "venue":
            dest = self.model["venues"]
            ext_dest = self.venue_ids
        if obj["type"] == "show":
            dest = self.model["shows"]
            ext_dest = self.show_ids
        if obj["type"] == "artist":
            dest = self.model["artists"]
            ext_dest = self.artist_ids
        if obj["id"] not in dest:
            try:
                dest.append(obj["id"])
                success = True
            except:
                self.log("append_global_id", "err", error_code=1)
                print("1")
        if obj["id"] not in ext_dest and obj["extant"] == True:
            try:
                ext_dest.append(obj["id"])
                success = True
            except:
                self.log("append_global_id", "err", error_code=2)
        return success

    def append_local_id(self, obj):
        """
        add entity id (obj input variable) to appropriate local locations
        (nested objects named by location) in the global object
        """
        success = False
        if obj["type"] == "venue":
            dest = self.model[obj["loc"]]["venue_ids"]
        if obj["type"] == "artist":
            dest = self.model[obj["loc"]]["artist_ids"]
        if obj["type"] == "show":
            dest = self.model[obj["loc"]]["shows"]["ids"]
        if obj["id"] not in dest:
            try:
                dest.append(obj["id"])
                self.locs[obj["loc"]] = self.model[obj["loc"]]
                success = True
            except:
                self.log("append_global_id", "err", error_code=3)
        return success

    def append_local_id_object(self, obj):
        """
        add entity as object to appropriate local locations (nested objects 
        named by location) in the global object
        """
        success = False
        if obj["type"] == "venue":
            dest = self.model[obj["loc"]]["venues"]
        if obj["type"] == "artist":
            dest = self.model[obj["loc"]]["artists"]
        if obj["type"] in ["venue", "artist"]:
            if obj["id"] not in dest:
                try:
                    dest[obj["id"]] = {"shows": []}
                    self.locs[obj["loc"]]
                    success = True
                except:
                    self.log("append_local_id_object", "err", error_code=5)
        if obj["type"] == "show":
            show_additions = 0
            dest1 = self.model[obj["loc"]]["venues"]
            try:
                dest[obj["id"]]["shows"].append(obj["id"])
                show_additions += 1
            except:
                self.log("append_local_id_object", "err", error_code=6)
            dest2 = self.model[obj["loc"]]["artists"]
            try:
                dest[obj["id"]]["shows"].append(obj["id"])
                show_additions += 1
            except:
                self.log("append_local_id_object", "err", error_code=7)
            if show_additions == 2:
                success == True
        return success

    def append_show_id_lists(self, obj):
        """
        ensure show ids from artist and venue selects are added to show lists
        """
        def append_show(show_id, local_list, global_list):
            if not show_id in local_list:
                local_list.append(show_id)
            if not show_id in global_list:
                global_list.append(show_id)

        success = False
        if obj["type"] == "artist":
            show_sublist = Select().get_artist_shows(obj["id"])
        if obj["type"] == "venue":
            show_sublist = Select().get_venue_shows(obj["id"])
        local_list = self.model[obj["loc"]]["shows"]["ids"]
        try:
            if not show_sublist is None and isinstance(show_sublist, list):
                for show_id in show_sublist:
                    append_show(show_id, local_list, self.model["shows"])
            self.locs[obj["loc"]]["shows"]["ids"] = local_list
            success = True
        except:
            self.log("", "err", error_code=8)
        return success

    def append_show(self, extant, loc, s_id):
        """
        """
        success = False
        placement = True
        obj = self.show_detail(s_id)
        obj["loc"] = loc
        try:
            a_dest = self.model[obj["loc"]]["artists"][obj["artist"]]
        except:
            self.log("", "err", error_code=10)
            placement = False
        try:
            v_dest = self.model[obj["loc"]]["venues"][obj["venue"]]
        except:
            self.log("append_show", "err", error_code=11)
            placement = False
        if placement == True:
            try:
                a_dest["shows"].append(obj["show_id"])
                a_dest[obj["start"]] = obj["show_id"]
                a_dest[obj["show_id"]] = obj
                success = True
            except:
                self.log("append_show", "err", error_code=12)
                success = False
            try:
                v_dest["shows"].append(obj["show_id"])
                v_dest[obj["start"]] = obj["show_id"]
                v_dest[obj["show_id"]] = obj
                success = True
            except:
                self.log("append_show", "err", error_code=13)
                success = False
        return success

    def show_detail(self, s_id):
        """
        form show_detail object
        """
        dtl = Select().get_show_detail(s_id)
        s_obj = {"venue": int(dtl[0]),
                    "artist": int(dtl[1]),
                    "start": dtl[2],
                    "end": dtl[3],
                    "show_id": int(s_id)}
        same_day = True
        if dtl[3].day != dtl[2].day:
            same_day = False
            second_start = datetime.datetime(dtl[3].year,
                                                dtl[3].month,
                                                dtl[3].day,
                                                1, 0, 0)
            s_obj["second_start"] = second_start
        return s_obj

    def new_genre(self, genre_name):
        """
        add unique genre to RdDb.genre_ids
        """
        self.log("call", "new_genre")
        if not genre_name in self.genres:
            # find id genre_name in genres database
            result = Select().verify_genre(genre_name)
            # if genre_name doesn't exist in the database, add it
            if result == False or result == -1:
                new_genre = Genre(genre_name)
                self.genre_ids.append(new_genre.id)
                self.genres[genre_name] = new_genre.id
                self.log("out", "new_genre", add=genre_name)
            else:
                self.log("out", "new_genre", find=genre_name)

#  ----------------------------------------------------------------------------
# / Command Line Control
# -----------------------------------------------------------------------------

class CliCtl:

    def __init__(self):
        """
        create cli session for populate
        """
        self.new_values = []
        self.new_genres = 0
        self.existing_genres = 0
        self.new_artists = 0
        self.existing_artists = 0
        self.new_venues = 0
        self.existing_venues = 0
        self.new_shows = 0
        self.existing_shows = 0
        global_obj.self_populate(self.delete_prompt())
        self.commit_genres()
        self.gen_entities(self.entity_prompt())
        logging.info("completed .__init__")

    def __repr__():
        """
        create string representation of CliCtl instance
        """
        msg = "CLI CTL\n" + str(self.ent)
        msg += "*"*20
        msg += "\n\n***\nnew genres: " + str(self.new_genres)
        msg += "\n\n***\nnew artists: " + str(self.new_artists)
        msg += "\n\n***\nnew venues: " + str(self.new_venues)
        msg += "\n\n***\nnew shows: " + str(self.new_shows)
        return msg

    def log(self, log_type, ftn_name, **kwargs):
        """
        creates log messages for CliCtl instance
        """
        info_msg = "CliCtl." + ftn_name
        if log_type == "call":
            info_msg = "called " + info_msg
        if log_type == "out":
            info_msg += " completed"
        if log_type == "err": 
            info_msg = info_msg + " failed with code "
            info_msg += str(kwargs["error_code"])
        logging.info(info_msg)

    @staticmethod
    def valid_int(int_floor, int_ceil, is_show):
        """
        ensures integer entered for entity_prompt is reasonable
        """
        logging.info("called CliCtl.valid_int")
        is_valid = False
        while is_valid == False:
            try:
                int_input = int(input(">> "))
                if (int_input >= int_floor) and (int_input < int_ceil):
                    is_valid = True
                elif int_input == 0:
                    is_valid = True
                else:
                    print("please enter a more reasonable integer")
                    print("input should be more than " + str(int_floor))
                    print("input should be less than " + str(int_ceil))
                if is_show:
                    msg = "remember: you are determining the number of shows "
                    msg += "that will be generated for each artist, not the "
                    msg += "total number of shows"
            except ValueError:
                print("input must be an integer")
        logging.debug("CliCtl.valid_int returning int_input" + str(int_input))
        logging.info("CliCtl.valid_int completed")
        return int_input

    def delete_prompt(self):
        """
        displays cli input menu to determine weather to clear db before running 
        program
        """
        delete_control = None
        blank_obj = None
        self.existing_venues = Select().count_total("venue")[0]
        self.existing_artists = Select().count_total("artist")[0]
        self.existing_shows = Select().count_total("show")[0]
        self.existing_values = self.existing_venues
        self.existing_values += self.existing_artists
        self.existing_values += self.existing_shows
        i = 0
        if self.existing_values > 0:
            while delete_control is None and i < 10:
                msg = "Database currently contains: "
                item = "\n    - {} {}"
                if self.existing_venues > 0: 
                    msg += item.format(str(self.existing_venues), "venues")
                if self.existing_artists > 0:
                    msg += item.format(str(self.existing_artists), "artists")
                if self.existing_shows > 0:
                    msg += item.format(str(self.existing_shows), "shows")
                print(msg)
                print("Would you like to clear all existing entities? (Y/n)")
                decision = input(">> ").lower()
                if decision in ["y", "n", "yes", "no"]:
                    if decision in ["y", "yes"]:
                        self.clear_db()
                        delete_control = True
                        blank_obj = True
                    if decision in ["n", 'no']:
                        delete_control = False
                        blank_obj = False
                else:
                    print("invalid input. Try again. \n\n")
                    i += 1
                    if i >= 9:
                        print("Too many invalid entries. Exiting program.")
        else:
            print("Database is currently empty")
            blank_obj = True
            delete_control = False
        return blank_obj

    def entity_prompt(self):
        """
        diplays cli input menu to get number of entities to create
        """
        logging.info("called CliCtl.entity_prompt")
        prompt = "\nEnter number of %s entities to create now:\n(%s already"
        prompt += " exist)"
        confirm_zero = "\nNo new %ss will be created"
        entities = [0, 0, 0]
        # prompt for n Artists
        if 'artists' in global_obj.model.keys():
            print(prompt % ("Artist", str(len(global_obj.model["artists"]))))
        new_artists = self.valid_int(1, 1000, False)
        if new_artists == 0:
            print(confirm_zero % ("artist"))
        entities[0] = new_artists
        # prompt for n Venues
        if 'venues' in global_obj.model.keys():
            print(prompt % ("Venue", str(len(global_obj.model["venues"]))))
        new_venues = self.valid_int(1, 1000, False)
        if new_venues == 0:
            print(confirm_zero % ("genre"))
        entities[1] = new_venues
        # 
        if 'shows' in global_obj.model.keys():
            print(prompt % ("Show", str(len(global_obj.model["shows"]))))
            new_shows = self.valid_int(1, 20, True)
            if new_shows == 0:
                print(confirm_zero % ("show"))
            entities[2] = new_shows
        print("entity_prompt returning " + str(entities))
        logging.debug("CliCtl.entity_prompt returning entites" + str(entities))
        logging.info("CliCtl.entity_prompt completed")
        return entities

    def gen_entities(self, entities):
        """
        generate Artist, Venue and Show entities
        number of entities created depends on DbData.entity_prompt()
        """
        def match_count(goal, ent_type):
            """
            subroutine used to add new Artist & Venue entities to CliCtl.rd_data 
                dict (by location) and to CliCtl.
            """
            new_entities = 0
            backup_count = 0
            success = False
            while new_entities < goal and backup_count < goal * 5:
                print("tried")
                ent = None
                if ent_type == "artist":
                    ent = self.make_artist()
                if ent_type == "venue":
                    ent = self.make_venue()
                if not ent is None:
                    self.new_values.append(ent)
                    new_entities += 1
                backup_count += 1
            if new_entities == goal:
                success = True
            return success

        logging.info("called CliCtl.gen_entities")
        msg = "Generating "
        msg += str(entities[0]) + " Artist entities"
        msg += ", " + str(entities[1]) + " Venue entities"
        msg += ", " + str(entities[2]) + " Show entities."
        print(msg)
        loop_control = True
        print(loop_control)
        if entities[0] > 0:
            loop_control = match_count(entities[0], "artist")
            print(loop_control)
            entities[0] == loop_control
        if entities[1] > 0 and loop_control == True:
            loop_control = match_count(entities[1], "venue")
            print(loop_control)
            entities[1] == loop_control
        if entities[2] > 0 and loop_control:
            loop_control == self.make_all_shows(entities[2])
            print(loop_control)
            entities[2] == loop_control
        logging.debug("CliCtl.gen_entities returning None (default)")
        logging.info("CliCtl.gen_entities completed")

    def make_artist(self):
        ent = Artist()
        print(ent.__repr__)
        if isinstance(ent.id, int) and ent.id > 0:
            print("tried")
            status = global_obj.append_artist(False, ent.city, ent.id)
            if status == True:
                self.new_artists += 1
                self.new_values.append(ent)
            else:
                self.log("make_artist", "err", error_code=14)
                ent = None
        else:
            self.log("make_artist", "err", error_code=16)
            ent = None
        return ent

    def make_venue(self):
        ent = Venue()
        if isinstance(ent.id, int) and ent.id > 0:
            status = global_obj.append_venue(False, ent.city, ent.id)
            if status == True:
                self.new_venues += 1
                self.new_values.append(ent)
            else:
                self.log("make_venue", "err", error_code=17)
                ent = None
        else:
            self.log("make_venue", "err", error_code=18)
            ent = None
        return ent

    def make_show(self, source_type, source_id):
        if source_type in ["artist", "venue"]:
            if source_type == "artist":
                ent = Show(artist_id=source_id)
            if source_type == "venue":
                ent = Show(venue_id=source_id)
        else:
            self.log("make_show", "err", error_code=1)
            ent = None
        if isinstance(show.id, int and ent.id > 0):
            status = global_obj.append_show(False, ent.city, ent.id)
            if status == True:
                self.new_shows += 1
                self.new_values.append(ent)
            else:
                self.log("make_shows", "err", error_code=19)
                ent = None
        else:
            self.log("make_shows", "err", error_code=20)
            ent = None
        return ent

    def make_shows(self, obj):
        """
        create not-very-random number of shows based on select for either
        artist or venue entity; called from CliCtl.make_all_shows
        """
        show_counter = 0
        backup_counter = 0
        msg = " shows for " + obj["source"] + " # " + str(obj["source_id"])
        while show_counter < obj["goal"] and backup_counter < obj["goal"]*5:
            if obj["source"] == "artist":
                ent = Show(artist_id=obj["source_id"])
            if obj["source"] == "venue":
                ent = Show(venue_id=obj["source_id"])
            if isinstance(ent.id, int) and ent.id > 0:
                show_counter += 1
            backup_counter += 1
        if show_counter == obj["goal"]:
            return show_counter
        else:
            return None

    def make_all_shows(self, amount):
        """
        create slightly randomized number of shows for all existing artist
        and venue entities
        """
        if amount < 3:
            amount = 3
        s_list = []
        failures = []
        total_shows = 0
        for a_id in global_obj.model["artists"]:
            s_list.append([a_id, "artist", len(Select().get_artist_shows(a_id))])
        for v_id in global_obj.model["venues"]:
            s_list.append([v_id, "venue", len(Select().get_venue_shows(v_id))])
        for item in s_list:
            obj = {"source": item[1],
                    "source_id": item[0],
                    "goal": random.choice(range(amount, amount+5)) - item[2]}
            result = self.make_shows(obj)
            if result is None:
                failures.append(obj)
            if isinstance(result, int):
                total_shows += result
        return [total_shows, failures]

    def decide_amount(self, amount):
        """
        decide the amount of shows that will actually be created for an entity
        """
        amount_top = amount + 4
        if (amount - 4) < 3:
            amount_bottom = 3
        else:
            amount_bottom = amount-4
        amount = random.choice(range(amount_bottom, amount_top))
        return amount

    def correlate_genres(self):
        """
        ensures each artist and venue has correlating ArtistGenre and VenueGenre
        runs after initial population
        """
        __init__(self):
            

    @staticmethod
    def clear_db():
        """
        delete every existing record from the database
        """
        successes = 0
        for entity in ["show", "artist", "venue", "genre"]:
            query = "DELETE FROM " + entity + ";"
            result = DbData("delete", query)
            if result == "success":
                successes += 1

    def commit_genres(self):
        """
        commit list of existing genres to the database if they aren't already
        in the database
        """
        genre_count = Select().count_total("genre")[0]
        self.log("call", "commit_genres")
        if genre_count < len(RdDb.genre_list):
            existing_genres = []
            for genre_name in RdDb.genre_list:
                if not genre_name in global_obj.genres:
                    genre_id = None
                    backup_count = 0
                    while genre_id is None and backup_count < 10:
                        genre = Genre(genre_name)
                        genre_id = genre.id
                        backup_count += 1
                    if isinstance(genre_id, int) and genre_id > 0:
                        global_obj.genres[genre_name] = genre_id
                        global_obj.genre_ids.append(genre_id)
                        self.new_values.append("g_" + str(genre_id))
                        self.new_genres += 1
                else:
                    existing_genres.append(genre_name)
        else:
            existing_genres = RdDb.genre_list[::]
        for genre_name in existing_genres:
            genre_id = Select().verify_genre(genre_name)
            if isinstance(genre_id, list) and len(genre_id) == 1:
                global_obj.genres[genre_name] = genre_id[0]
                global_obj.genre_ids.append(genre_id[0])
        self.log("out", "commit_genres")

#  ----------------------------------------------------------------------------
# / Database modification & retrieval classes for psycopg2
# -----------------------------------------------------------------------------

class DbData:
    """
    contains modules for adding new entities to database and validating that
    it does not already exist in the database
    """

    def __init__(self, *args):
        """
        init instance of DbData class
        """
        self.class_name = args[0]
        self.active = False # boolean if 
        self.error = False # boolean
        self.status = 0
        self.result = None # contains query result
        self.res_list = None
        self.query = ""
        self.value_list = []
        if len(args) > 0:
            if args[0] == "delete":
                self.query = args[1]
                self.result = self.delete(self.query)
        logging.info("completed DbData.__init__")

    def err(self, err, exc_info, msg):
        """
        detailed error log for DbData class and its descendents
        """
        self.status = -1
        self.error = {"info": exc_info[1],
                    "msg": msg}
        if not err is None:
            self.error["psycopg2_error"] = '{}'.format(err)
        logging.error(self.error)
        self.result = False
        return err

    def delete(self, query):
        """
        Delete all records in a specified table
        """
        self.query = query
        self.log("call", "delete")
        self.query = query
        conn = psycopg2.connect("dbname=fyyur")
        cur = conn.cursor()
        self.active = True
        if len(self.query) > 0:
            try:
                cur.execute(self.query)
                self.result = "success"
                conn.commit()
                self.status = 1
            except BaseException as e:
                msg = "unspecified error"
                conn.rollback()
                self.result = self.err(None, sysinfo(), msg)
                self.status = 0
            finally:
                self.active = False
                cur.close()
                conn.close()
        self.log("out", "delete", result=self.result)
        if isinstance(self.result, int):
            return self.result
   
    def __repr__(self):
        """
        form string representation of DbData instance
        """
        # TODO: make lines of code shorter
        repr_iter = [
            ["active", "default" if not hasattr(self, "active") else str(self.active)],
            ["error", "default" if not hasattr(self, "error") else str(self.error)],
            ["status", "default" if not hasattr(self, "status") else str(self.status)],
            ["result", "default" if not hasattr(self, "result") else str(self.result)],
            ["value_list", "default" if not hasattr(self, "value_list") else str(self.value_list)],
            ["class_name", "default" if not hasattr(self, "class_name") else str(self.class_name)],
            ["query", "default" if not hasattr(self, "query") else str(self.query)]]

        msg = "\n=========== "
        if hasattr(self, "class_name"):
            if self.class_name == "select":
                msg += "SELECT"
            if self.class_name == "insert":
                msg += "INSERT"
            if self.class_name == "delete":
                msg += "DELETE"
        msg += " object =============================\n"
        for item in repr_iter:
            msg += "\n" + item[0] + ": " + str(item[1])
        if hasattr(self, "id"):
            msg += "\nid: " + str(self.id)
        msg += "\n=======================================================\n"
        return msg

    def log(self, log_type, ftn_name, **kwargs):
        """
        form log message for functions in DbData
        accepts args in [logging_type, ftn_name, class_name]
         - log_type: can be "call", "output" or None type
         - ftn_name: name of class function from which log was called
         - kwargs: lists objects updated or returned by function
        logs via python logging library
        """
        # set class_name
        if hasattr(self, "class_name"):
            if not self.class_name is None:
                class_name = str(self.class_name)
        else:
            class_name = "DbData"
        # 
        if log_type == "call":
            info_msg = "called " + class_name + "." + ftn_name
            if len(kwargs) > 0:
                info_msg += " using:  "
                for arg in kwargs.keys():
                    info_msg += "\n      - " + arg + " = " + str(kwargs[arg])
        if log_type == "out":
            info_msg = class_name + "." + ftn_name + " complete"
            if len(kwargs) > 0:
                debug_msg = class_name + "." + ftn_name + " updated: "
                for arg in kwargs.keys():
                    debug_msg += "\n      - self. " + arg + " to " 
                    debug_msg += str(kwargs[arg])
                logging.debug(debug_msg)
            summary = "  summary:"
            if hasattr(self, "query"):
                summary += "\n" + " " * 16 + "- query: " + self.query
            else:
                summary += "\n" + " " * 16 + "- query: none."
            if hasattr(self, "result"):
                summary += "\n" + " " * 16 + "- attributes: "
                summary += str(self.value_list)
            else:
                summary += "\n" + " " * 16 + "- attributes: none."
            if hasattr(self, "value_list"):
                summary += "\n " + " " * 16 + "- result: " + str(self.result)
            else:
                summary += "\n" + " " * 16 + "- result: none."
            summary += "\n" + " " * 16 + "- status: " + str(self.status)
            logging.debug(summary)
        logging.info(info_msg)

    def log_return(self, ftn_name, **kwargs):
        """
        """
        msg = " >> " + ftn_name + " returning "
        for arg in kwargs:
            if len(kwargs) > 1:
                msg += "\n       * "
            msg += arg + " = "
            if not kwargs[arg] is None:
                msg += str(kwargs[arg])
            else:
                msg += " None (type)"
        logging.debug(msg)

    def make(self):
        """
        execute INSERT QUERY; return ID
        """
        self.log("call", "make")
        conn = psycopg2.connect("dbname=fyyur")
        cur = conn.cursor()
        self.active = True
        if len(self.query) > 0:
            try:
                cur.execute(self.query, self.value_list)
                if self.query.find("RETURNING") > 0:
                    self.result = cur.fetchall()[0][0]
                else:
                    self.result = "success"
                conn.commit()
                self.status = 1
                self.error = False
            except psycopg2.OperationalError as e:
                msg = "unable to connect"
                conn.rollback()
                self.error = self.err(e, sysinfo(), msg)
                self.status = 0
            except psycopg2.IntegrityError as e:
                msg = "probably encountered unacceptable duplicate"
                conn.rollback()
                self.error = self.err(e, sysinfo(), msg)
                self.status = 0
            except BaseException as e:
                msg = "unspecified error"
                conn.rollback()
                self.error = self.err(None, sysinfo(), msg)
                self.status = 0
            finally:
                self.active = False
                cur.close()
                conn.close()
        self.log("out", "make", result=self.result)
        if self.status == 0:
            self.result = None
        if isinstance(self.result, int):
            return self.result

    def get(self):
        """
        execute SELECT query; return result list
        """
        self.log("call", "get")
        if len(self.query) > 0:
            conn = psycopg2.connect("dbname=fyyur")
            cur = conn.cursor()
            self.active = True
            try:
                if len(self.value_list) > 0:
                    cur.execute(self.query, self.value_list)
                else:
                    cur.execute(self.query)
                self.result = self.flatten(cur.fetchall())
                self.status = 1
            except psycopg2.OperationalError as e:
                msg = "unable to connect"
                self.result = self.err(e, sysinfo(), msg)
            except psycopg2.IntegrityError as e:
                msg = "probably encountered unacceptable duplicate"
                self.result = self.err(e, sysinfo(), msg)
            except BaseException as e:
                msg = "unspecified error"
                self.result = self.err(None, sysinfo(), msg)
            finally:
                self.active = False
                cur.close()
                conn.close()
        else:
            logging.info("DbData.self will not run on query " + str(self.query))
        result = []
        if isinstance(self.result, list):
            for item in self.result:
                if isinstance(item, tuple) and len(item)==1:
                    item = item[0]
                result.append(item)
            self.result = result
        self.log_return("get", result=result)
        return self.result

    @staticmethod
    def flatten(result):
        """
        return a formatted result for list results
        """
        flat = []
        if len(result) > 0:
            for record in result:
                if len(record) == 1:
                    for data in record:
                        flat.append(data)
                else:
                    if len(result) == 1:
                        for data in record:
                            flat.append(data)
                    elif len(result) > 1:
                        tuple_list = []
                        for data in record:
                            tuple_list.append(data)
                        flat.append(data)
        return flat

    def ins_query(self, ent):
        """
        generates insert query for single item
        """
        query = 'INSERT INTO ' + ent.entity_type + ' '
        cols = "("
        vals = ") VALUES ("
        val_list = []
        for attr in ent:
            if attr[0] != "entity_type":
                cols += attr[0] + ", "
                vals += '%s, '
                val_list.append(attr[1])
        query += cols[:-2] + vals[:-2]
        query += ") RETURNING id;"
        self.query = query
        self.value_list = val_list

    @staticmethod
    def cln_str(attr_list):
        """
        clean attribute string, removing ' and "
        """
        i = 0
        while i < len(attr_list):
            if (str(type(attr_list)) == "<class 'str'>"):
                if attr_list[i].find("'") < -1:
                    attr_list[i].replace("'", "''")
            i += 1
        return attr_list

    @staticmethod
    def get_entity(ent):
        """
        get id from specific Artist or Venue entity
        """
        logging.info("called DbData.get_entity")
        query = "SELECT id FROM " + ent.entity_type + " WHERE "
        query += "name=%s AND phone=%s;"
        debug_msg = "DbData.get_entity returning 'tuple': "
        debug_msg += str((query, [ent.name, ent.phone], ent.entity_type))
        logging.debug(debug_msg)
        logging.info("completed DbData.")
        return (query, [ent.name, ent.phone], ent.entity_type)       

class Select(DbData):
    """
    functions and methods for db selects
    """

    def __init__(self):
        """
        init object of class select query
        generate queries based on specific needs for selecting automatically
          generated entities
        """
        super().__init__("select")
        self.id = -1
        if isinstance(self.result, int) and self.id > 0:
            self.id = self.result
        logging.info("completed Select.__init__")

    def get_entity_ids(self, entity_name):
        """
        get list of entity ids from a specifed entity
        """
        self.log("call", "get_entity_ids")
        self.query = 'SELECT id FROM "' + entity_name + '";'
        self.result = self.get()
        self.log_return("get_entity_ids", kind=entity_name, ids=self.result)
        self.log("out", "get_entity_ids")
        return self.result

    def loc_search(self, location):
        """
        returns a tuple with list of venue and artist ids of entities that exist
            in a location
        """
        self.log("call", "loc_search")
        self.query = "SELECT id FROM venue WHERE city=%s;"
        self.value_list = [location]
        result_list = [self.get()]
        self.query = "SELECT id FROM artist WHERE city=%s;"
        result_list.append(self.get())
        self.log_return("loc_search", 
                            venue_ids=result_list[0],
                            artist_ids=result_list[1])
        self.log("out", "loc_search")
        return result_list

    def get_location(self, entity_name, ent_id):
        """
        returns location string for venue or artist id if it is a default 
            location
        """
        self.log("call", "get_location", name=entity_name, id=ent_id)
        self.query = "SELECT city, state FROM " + entity_name + " WHERE id=%s;"
        self.value_list = [ent_id]
        result = self.get()
        if not isinstance(result, str) and not result is None:
            if result in RdDb.location_names:
                self.result = result
        self.log_return("get_location", location=self.result)
        self.log("out", "get_location")
        return self.result

    def get_venue_shows(self, venue_id):
        """
        get ids of shows where venue id matches specified param
        """
        self.log("call", "get_venue_shows", id=venue_id)
        self.query = "SELECT id FROM show WHERE venue_id=%s;"
        self.value_list = [venue_id]
        vlist = self.get()
        if isinstance(vlist, int):
            vlist = [vlist]
        self.log_return("get_venue_shows", shows=vlist)
        self.log("out", "get_venue_shows")
        return vlist

    def get_artist_shows(self, artist_id):
        """
        get ids of shows where artist id matches specified param
        """
        self.log("call", "get_artist_shows", id=artist_id)
        self.query = "SELECT id FROM show WHERE artist_id=%s;"
        self.value_list = [artist_id]
        alist = self.get()
        if isinstance(alist, int):
            alist = [alist]
        self.log_return("get_venue_shows", shows=alist)
        self.log("out", "get_venue_shows")
        return alist

    def count_total(self, entity_name):
        """
        return total number of entity specified by entity_name in database
        """
        self.log("call", "count_total")
        self.query = "SELECT count(id) FROM " + entity_name + ";"
        total = self.get()
        self.log("out", "count_total")
        return total

    def get_show_detail(self, show_id):
        """
        get additional information for a show with a specified id
        """
        self.log("call", "get_show_detail", show_id=show_id)
        self.query = "SELECT venue_id, artist_id, start_time, end_time FROM "
        self.query += " show WHERE id=%s;"
        self.value_list = [show_id]
        result = self.get()
        return result

    def verify_genre(self, genre_name):
        """
        get name of specified name from genres
        """
        self.log("call", "verify_genre")
        self.query = "SELECT id FROM genre WHERE name=%s;"
        self.value_list = [genre_name]
        self.result = self.get()
        self.log_return("verify_genre", genre_id=self.result)
        self.log("out", "verify_genre")
        return self.result

    def get_genre(self, genre_id):
        """
        get name of genre with specified id from genres 
        """
        self.log("call", "get_genre")
        self.query = "SELECT name FROM genre WHERE id=%s;"
        self.value_list = [genre_id]
        self.result = self.get()
        self.log_return("get_genre", genre=self.result)
        self.log("out", "genre_id")
        return self.result

    def get_genres(self):
        """
        get names of all genres that exist in the database
        """
        self.log("call", "get_genres")
        self.query = "SELECT name FROM genre;"
        self.result = self.get()
        self.log_return("get_genres", genres=self.result)
        self.log("out", "get_genres")
        return self.result

class Insert(DbData):
    """
    functions and methods for db selects
    """

    def __init__(self, entity):
        """
        init object of class select query
        generate queries based on specific needs for selecting automatically
          generated entities
        """
        entity.__repr__()
        DbData.__init__(self, "insert", None)
        self.ins_query(entity)
        self.make()
        if not self.result is None and self.result > 0:
            self.id = self.result
        else:
            self.id = -2

#  ----------------------------------------------------------------------------
# // Random Entity Object Classes                                            //
# ----------------------------------------------------------------------------

class Entity:
    """
    Generate Attributes common to Artist and Venue Classes
    """

    def __init__(self, *args):
        """
        init instance of Entity class
        """
        location = RdDb.new_location(-1)
        if not args is None and len(args) == 1:
            if args[0] in RdDb.location_names:
                location = RdDb.new_location(args[0])
        self.city = location["city"]
        self.state = location["state"]
        self.phone = RdDb.new_phone(location["area_code"])
        self.genre_list = RdDb.new_genres()
        self.genres = self.string_genres()
        self.has_image = True
        self.is_seeking = random.choice([True, False])
        logging.info("completed Entity.__init__")
    
    def string_genres(self):
        genre_string = ""
        for genre in self.genre_list:
            genre_string += genre + ","
        return genre_string[:-1]

    def log(self, log_type, ftn_name, **kwargs):
        """
        form log for functions in Entity class and its descendants
        """
        msg = self.entity_type[0].upper() + self.entity_type[1:] + "."
        msg += ftn_name + " "
        if log_type == "call":
            info_msg = "called " + msg + " using "
            for arg in kwargs.keys():
                info_msg += "\n      - " + arg + " = " + str(kwargs[arg])
        if log_type == "out":
            info_msg = msg + "complete."
            if len(kwargs) > 0:
                debug_msg = class_name + "." + ftn_name + " updated: "
                for arg in kwargs.keys():
                    debug_msg += "\n      - self. " + arg + " to " 
                    debug_msg += str(kwargs[arg])
                logging.debug(debug_msg)
                logging.debug(self.__repr__())
            logging.log(debug_msg)
        logging.info(info_msg)

# --- Artist entity object class ----------------------------------------------

class Artist(Entity, DbData):
    """
    Generate new Artist object populated with random data to be used
    as attributes for a Artist entity
    """
    attribute_list = ["entity_type", "city", "state", "phone",
        "genre_list", "name", "facebook_link", "website_link", "is_seeking",
        "seeking_description", "has_image", "image_link"]

    def __init__(self, *args):
        """
        Generate new Artist object populated with random data to be used
        as attributes for an Artist entity
        """
        # pylint: disable=too-many-instance-attributes
        # one attribute is used for each required db entity attribute
        # program is not complex or neccessary enough to re-design
        if not args is None and len(args) == 1:
            Entity.__init__(self, args)
        else:
            Entity.__init__(self)
        self.entity_type = "artist"
        self.name = self.generate_artist_name()
        string_name = RdDb.uris(self.name)
        self.facebook_link = string_name[0]
        self.website_link = string_name[1]
        self.seeking_description = self.seeking_desc(self.is_seeking)
        self.image_link = self.new_image_link()
        query = self.ins_query(self)
        insert_obj = Insert(self)
        self.id = insert_obj.id
        logging.info("completed Artist.__init__")
        if isinstance(self.id, int) and self.id > 0:
            self.relate_genres()

    def __repr__(self):
        """
        Display attributes generated for Artist object
        """

        try:
            msg = "\n\nARTIST ENTITY" + "\n"
            msg += "================================================"*2 + "\n"
            msg += "name: " + self.name + " | id: " + str(self.id) + "\n"
            msg += "city: " + self.city + ", state: " + self.state + "\n"
            msg += "phone: " + self.phone + "\n"
            msg += "website: " + self.website_link + "\n"
            msg += "fb link: " + self.facebook_link + "\n"
            if self.is_seeking:
                msg += "Seeking talent (" + self.seeking_description + ")\n"
            else:
                msg += "Not seeking talent." 
            msg += self.seeking_description + ")\n"
            msg += "image_link exists and has " + str(int(len(self.image_link)))
            msg += "================================================"*2 + "\n"
            msg += "genres: " + str(self.genre_list) + "\n"
            msg += "================================================"*2 + "\n"
        except:
            msg += "incomplete artist entity."
        finally:
            return msg + "\n\n"

    def __iter__(self):
        yield ("city", self.city)
        yield ("state", self.state)
        yield ("phone", self.phone)
        yield ("genres", self.genres)
        yield ("has_image", self.has_image)
        yield ("is_seeking", self.is_seeking)
        yield ("name", self.name)
        yield ("facebook_link", self.facebook_link)
        yield ("seeking_description", self.seeking_description)
        yield ("website_link", self.website_link)
        yield ("image_link", self.image_link)

    def generate_artist_name(self):
        """
        returns name for artist entity based on random choices from RdDb
        information
        """
        logging.info("Artist.generate_venue_name")
        def full_name(self):
            """
            returns a random first name from list of first names and last
            name from list of last names
            """
            r_names = RdDb.new_person_name()
            return r_names[0] + " " + r_names[1]

        def full_name_and(self):
            """
            returns randomized full name from fullName() with a plural noun
            """
            r_names = RdDb.new_person_name()
            band_name = r_names[0] + " " + r_names[1]
            plural = RdDb.new_band_word([3])[0]
            return band_name + " and the " + plural

        def full_name_band(self):
            """
            returns a name based on the pattern The <fullName> band.
            fullName is generated by the fullName() function
            """
            r_names = RdDb.new_person_name()
            return "The " + r_names[0] + " " + r_names[1] + " Band"

        def nickname_and_thes(self):
            """
            returns a name combining a randomly selected nickname from a
            list of nicknames and a plural noun
            """
            nickname = random.choice(RdDb.names['nicknames'])
            plural = RdDb.new_band_word([3])[0]
            return nickname + " and the " + plural

        def two_word(self):
            """
            returns a name combining an adjective from a list of adjectives
            (firstWord) and a plural noun from a list of plural nouns
            (secondWord)
            """
            words = RdDb.new_band_word([2, 3])
            return words[0] + " " + words[1]

        def three_word(self):
            """
            returns a name combining two adjectives from two lists of
            adjectives (firstWord and secondWord) and a plural noun from a
            list of plural nouns (thirdWord)
            """
            words = RdDb.new_band_word([1, 2, 3])
            return words[0] + " " + words[1] + " " + words[2]

        def single_word(self):
            """
            returns a name randomly selected from a list of strings
            """
            return RdDb.new_band_word([0])[0]

        name_choice = random.choice(range(1, 11))
        if name_choice == 1:
            logging.debug("   -> full name from 1")
            name = full_name(self)
        if name_choice == 2:
            logging.debug("   -> full name 'and' from 2")
            name = full_name_and(self)
        if name_choice == 3:
            logging.debug("   -> full name 'band' from 3")
            name = full_name_band(self)
        if name_choice == 4:
            logging.debug("   -> full name nickname 'and' from 4")
            name = nickname_and_thes(self)
        if name_choice in (5, 6):
            logging.debug("   -> two word from 5, 6")
            name = two_word(self)
        if name_choice in (7, 8):
            logging.debug("   -> three word from 7, 8")
            name = three_word(self)
        if name_choice in (9, 10):
            logging.debug("   -> single world from 9, 10")
            name = single_word(self)
        logging.debug("Artist.generate_venue_name to return " + str(name))
        logging.info("Artist.generate_venue_name completed")
        return name

    @staticmethod
    def seeking_desc(flip):
        """
        return tuple containing boolean if artist is seeking performance space
        and a default message to display
        """
        if flip:
            desc = "We are seeking venues for our upcoming concert schedule."
        else:
            desc = "Our upcoming schedule has already been filled and we do"
            desc = desc + " not currently need to find space."
        logging.debug("Artist.seeking_desc to return " + str(desc))
        logging.info("Artist.seeking_desc completed")
        return desc

    def new_image_link(self):
        """
        returns image link from small set of image links for display on Artist
        page
        """
        logging.debug("Artist.new_image_link completed")
        return random.choice(RdDb.artist_images)

    def relate_genres(self):
        for genre in self.genre_list:
            rel_id = ArtistGenre(global_obj.genres[genre], self.id)

# --- Venue entity object class -----------------------------------------------

class Venue(Entity, DbData):
    """
    Contains __init__ method to form a Venue entity populated with randomized
    data and methods specific to Venue entity attributes
    """
    attribute_list = ["entity_type", "city", "state", "phone",
        "genre_list", "address", "name", "facebook_link", "website_link",
        "is_seeking","seeking_description", "has_image", "image_link"]
    id_list = []
    logging.info("completed Venue.__init__")

    def __init__(self, *args):
        """
        Generate new Venue object populated with random data to be used
        as attributes for a Venue entity
        """
        # pylint: disable=too-many-instance-attributes
        # one attribute is used for each required db entity attribute
        # program is not complex or neccessary enough to re-design
        self.entity_type = "venue"
        if not args is None and len(args) == 1:
            Entity.__init__(self, args)
        else:
            Entity.__init__(self)
        self.entity_type = "venue"
        addr = RdDb.new_address()
        self.address = addr["address"]
        self.name = self.generate_name(addr)
        string_name = RdDb.uris(self.name)
        self.facebook_link = string_name[0]
        self.website_link = string_name[1]
        self.seeking_description = self.seeking_desc(self.is_seeking)
        self.image_link = self.new_image_link()
        insert_obj = Insert(self)
        self.id = insert_obj.id
        if isinstance(self.id, int) and self.id > 0:
            self.relate_genres()
        logging.debug("called Venue.__init__")

    def __repr__(self):
        """
        Display attributes generated for Venue object
        """
        # TODO: make shorter
        repr_iter = [["city", 
            "none." if not hasattr(self, "city") else str(self.city)],
        ["state", 
            "none." if not hasattr(self, "state") else str(self.state)],
        ["phone", 
            "none." if not hasattr(self, "phone") else str(self.phone)],
        ["genre_list", 
            "none." if not hasattr(self, "genre_list") else str(self.genre_list)],
        ["has_image", 
            "none." if not hasattr(self, "has_image") else str(self.has_image)],
        ["is_seeking", 
            "none." if not hasattr(self, "is_seeking") else str(self.is_seeking)],
        ["entity_type", 
            "none." if not hasattr(self, "entity_type") else str(self.entity_type)],
        ["address", 
            "none." if not hasattr(self, "address") else str(self.address)],
        ["name", 
            "none." if not hasattr(self, "name") else str(self.name)],
        ["facebook_link", 
            "none." if not hasattr(self, "facebook_link") else str(self.facebook_link)],
        ["seeking_description", 
            "none." if not hasattr(self, "seeking_description") else str(self.seeking_description)],
        ["image_link", 
            "none." if not hasattr(self, "image_link") else str(self.image_link)],
        ["id", 
            "none." if not hasattr(self, "id") else str(self.id)]]     

        try:
            msg = "\n\nVenue ENTITY\n"
            msg += "================================================"*2 + "\n"
            msg += "name: " + self.name + "\n"
            msg += "address: " + self.address + "\n"
            msg += "city: " + self.city + ", state: " + self.state + "\n"
            msg += "phone: " + self.phone + "\n"
            msg += "website: " + self.website_link + "\n"
            msg += "fb link: " + self.facebook_link + "\n"
            if self.is_seeking:
                msg += ("Seeking talent (" + self.seeking_description + ")")
            else: 
                msg += ("Not seeking talent (" + self.seeking_description + ")")
            msg += "image link: " + str(self.image_link) + "\n"
            msg += "================================================"*2 + "\n"
            msg += "genres: " + str(self.genre_list) + "\n"
            msg += "================================================"*2 + "\n"
        except:
            msg = "incomplete VENUE entity\n"
            msg += "================================================"*2 + "\n"
        finally:
            return msg + "\n\n"

    def __iter__(self):
        yield ("address", self.address)
        yield ("city", self.city)
        yield ("state", self.state)
        yield ("phone", self.phone)
        yield ("genres", self.genres)
        yield ("has_image", self.has_image)
        yield ("is_seeking", self.is_seeking)
        yield ("name", self.name)
        yield ("facebook_link", self.facebook_link)
        yield ("seeking_description", self.seeking_description)
        yield ("website_link", self.website_link)
        yield ("image_link", self.image_link)

    def generate_name(self, addr):
        """
        determines Venue name format based on the return of random.choice()
        accepts address as init parameters
        """
        logging.info("called Venue.")
        def possessive(option):
            """
            returns name based on a random last name. Simple; possessive is
            added. If option is False, returns the posessive as a description
            of a venue type
            """
            last_name = RdDb.new_person_name()[1] + "'"
            if last_name[-1] != "s":
                venue_name = last_name + "s"
            if option is False:
                venue_type = RdDb.new_venue_type()
                venue_name = venue_name + " " + venue_type
            return venue_name

        def genre_based(genres, street):
            """
            returns a name based on a genre in the genre_list
            """
            genre = random.choice(genres)
            venue_type = RdDb.new_venue_type()
            flip = random.choice([True, False])
            if flip:
                venue_name = possessive(True) + " " + genre + " " + venue_type
            else:
                venue_name = street + " " + genre + " " + venue_type
            return venue_name

        def location_based(city):
            """
            returns a venue name based on the city from the Factory object used
            to create it
            """
            flip = random.choice([True, False])
            venue_name = city + " "
            venue_type = RdDb.new_venue_type()
            if flip:
                venue_name = venue_name + random.choice(self.genre_list) + " "
            venue_name = venue_name + " " + venue_type
            return venue_name

        def street_based(genres, addr):
            """
            returns a venue name based on the streetname of the address
            generated within the Venue class
            """
            genre = random.choice(genres)
            venue_type = RdDb.new_venue_type()
            roll = random.choice(["a", "b", "c"])
            if roll=="a":
                venue_name = addr["street"] + " " + venue_type
            elif roll=="b":
                venue_name = addr["street"] + " " + genre + " " + venue_type
            elif roll=="c":
                street_sublist = [ "Second", "Third", "First", "Fourth", "Park",
                    "Fifth", "Main", "Sixth", "Oak", "Seventh", "Pine",
                    "Eighth", "Washington", "Ninth", "Broad", "Ridge", "Cherry"]
                if addr["short_street"] in street_sublist:
                    venue_name = venue_type
                else:
                    venue_name = genre + " " + venue_type
                venue_name = venue_name + " on " + addr["short_street"]
            return venue_name

        roll = random.choice(range(1, 6))
        if roll == 1:
            name = possessive(True)
        elif roll == 2:
            name = genre_based(self.genre_list, addr["street"])
        elif roll == 3:
            name = possessive(False)
        elif roll == 4:
            name = location_based(self.city)
        elif roll == 5:
            name = street_based(self.genre_list, addr)
        return name

    @staticmethod
    def seeking_desc(flip):
        """
        return tuple containing boolean if venue is seeking talent and a default
        message to display
        """
        logging.info("called Venue.")
        if flip:
            desc = "We encourage artists seeking a venue to schedule via the"
            desc = desc + " fyyur app."
        else:
            desc = "We are currently fully booked for our available schedule."
        return desc

    def new_image_link(self):
        """
        returns image link from small set of image links for display on Artist
        page
        """
        logging.info("called Venue.new_image_link")
        return random.choice(RdDb.venue_images)

    def relate_genres(self):
        for genre in self.genre_list:
            rel_id = VenueGenre(global_obj.genres[genre], self.id)

# --- Show entity object class ------------------------------------------------

class Show(DbData):
    """
    adds additional class attributes to Event object
    """
    session_redef = 0
    logging.info("completed Show.__init__")

    def __init__(self, **kwargs):
        """
        returns instance of Show object
        """
        self.venue_id = -1
        self.artist_id = -1
        self.entity_type = "show"
        self.all_day = False
        if not kwargs is None:
            self.init_control = self.set_given_ids(kwargs)
            if self.init_control == True:
                self.init_control = self.get_location()
            if self.init_control == True:
                self.init_control = self.get_other_id()
            if self.init_control == True:
                self.init_control = self.schedule()
            if self.init_control == True:
                self.id = Insert(self).id
            else:
                self.id = -1

    def __repr__(self):
        try:
            msg = "\n\n=============================================="*2 + "\n"
            msg += "SHOW entity: \n"
            if self.id > 0:
                msg += "id is " + str(self.id) + "\n"
            msg += "venue_id: " + str(self.venue_id) + " & "
            msg += "artist_id: " + str(self.artist_id) + "\n"
            msg += "@ " + str(self.start_time) + " - " + str(self.end_time)
            msg += "(" + str(self.all_day) + ")"
            msg += "================================================"*2 + "\n"
        except:
            msg = "incomplete SHOW entity"
        finally:
            return msg

    def __iter__(self):
        if hasattr(self, "init_control") and self.init_control == True:
            if hasattr(self, "venue_id"):
                yield ("venue_id", self.venue_id)
            if hasattr(self, "artist_id"):
                yield ("artist_id", self.artist_id)
            if hasattr(self, "start_time"):
                yield ("start_time", self.start_time)
            if hasattr(self, "end_time"):
                yield ("end_time", self.end_time)
            if hasattr(self, "all_day"):
                yield ("all_day", self.all_day)

    def log(self, log_type, ftn_name, **kwargs):
        info_msg = "Show." + ftn_name
        for arg in kwargs:
            vals = ": "
            if arg != "init_control":
                vals += "\n" + (6*" ") + "- " + arg + ": "
                vals += str(kwargs[arg])
        if log_type == "call":
            info_msg = "Called " + info_msg
            if len(kwargs.keys()) > 0:
                debug_msg = "new values: " + str(kwargs)
                logging.debug(debug_msg)
        if log_type == "out":
            info_msg += " completed. "
            if len(kwargs.keys()) > 0:
                debug_msg = "new values: " + vals
                logging.debug(debug_msg)
        if "init_control" in kwargs.keys():
                init_msg = "init control is "
                init_msg += str(kwargs["init_control"]) + " following Show." 
                init_msg += ftn_name
                logging.debug(init_msg)
        logging.info(info_msg)

    def set_given_ids(self, kwargs):
        self.init_control = True
        self.log("call", "set_given_ids")
        if "venue_id" in kwargs.keys():
            if isinstance(kwargs["venue_id"], int):
                self.venue_id = kwargs['venue_id']
            else:
                self.init_control = False
            if "artist_id" in kwargs.keys():
                self.init_type = "dual"
                if isinstance(kwargs["artist_id"], int):
                    self.artist_id = kwargs["artist_id"]
                else:
                    self.init_control = False
            else:
                self.init_type = "venue"
        elif "artist_id" in kwargs.keys():
            if isinstance(kwargs["artist_id"], int):
                self.artist_id = kwargs["artist_id"]
                self.init_type = "artist"
            else:
                self.init_control = False
        self.log("out", 
                    "set_given_ids", 
                    init_control=self.init_control,
                    venue_id=self.venue_id,
                    artist_id=self.artist_id,
                    init_type=self.init_type)
        return self.init_control

    def get_other_id(self):
        init_control = True
        self.log("call",
            "set_given_ids",
            city = self.city,
            artist_id = self.artist_id,
            venue_id = self.venue_id,
            init_type = self.init_type)
        if not isinstance(self.city, str) or len(self.city) < 1:
            init_control = False
        if not self.init_type in ["venue", "artist"]:
            init_control = False
        else:
            sel = "artist_ids" if self.init_type=="venue" else "venue_ids"
        # select pair id
        if init_control == True:
            pair_id = None
            if len(global_obj.locs[self.city][sel]) > 0:
                pair_id = random.choice(global_obj.locs[self.city][sel])
                if self.init_type == "artist":
                    self.venue_id = pair_id
                if self.init_type == "venue":
                    self.artist_id = pair_id
            else:
                if self.init_type=="venue":
                    ent = Artist(self.city)
                    if isinstance(ent.id, int) and ent.id > 0:
                        self.artist_id = ent.id
                        global_obj.append_artist(False, self.city, ent.id)
                    else:
                        init_control = False
                if self.init_type=="artist":
                    ent = Venue(self.city)
                    if isinstance(ent.id, int) and ent.id > 0:
                        self.venue_id = ent.id
                        global_obj.append_venue(False, self.city, ent.id)
                    else:
                        init_control = False
        self.log("out",
            "get_other_id",
            init_control=self.init_control,
            venue_id=self.venue_id,
            artist_id=self.artist_id,
            init_type=self.init_type)
        return init_control

    def get_location(self):
        """
        """
        if self.init_control == False:
            return None
        success = False
        if self.init_type in ["venue", "dual"]:
            location = Select().get_location("venue", self.venue_id)
        elif self.init_type == "artist":
            location = Select().get_location("artist", self.artist_id)
        if not location is None and len(location) == 2:
            self.city = location[0]
            self.state = location[1]
            success = True
        self.log("out",
            "get_location",
            init_control=self.init_control,
            location=location,
            city=self.city,
            state=self.state)
        return success

    def schedule(self):
        """
        """
        dates = RdDb.new_schedule_item()
        self.start_time = dates[0]
        self.end_time = dates[1]
        self.log("out",
            "schedule",
            init_control=self.init_control)
        return True

# --- Genre entity object class -----------------------------------------------

class Genre(DbData):
    """
    stores variables and functions to store various genre names
    """

    def __init__(self, *args):
        """
        """
        self.entity_type = "genre"
        self.name = None
        if len(args) == 1:
            if isinstance(args[0], str):
                self.name = args[0]
                self.id = Insert(self).id
        logging.info("completed Genre.__init__")

    def __iter__(self):
        yield ("name", self.name)

# --- Artist Genre object class

class ArtistGenre(DbData):
    """
    relates artist_id and genre_id in record
    """

    def __init__(self, genre_id, artist_id):
        """
        init instance of ArtistGenre class
        """
        self.entity_type = "artist_genres"
        self.artist_id = artist_id
        self.genre_id = genre_id
        self.id = Insert(self).id

    def __iter__(self):
        yield("artist_id", self.artist_id)
        yield("genre_id", self.genre_id)

# --- Venue Genre object class

class VenueGenre(DbData):
    """
    relates artist_id and venue_id in record
    """

    def __init__(self, genre_id, venue_id):
        """
        instance of ArtistGenre class
        """
        self.entity_type = "venue_genres"
        self.venue_id = venue_id
        self.genre_id = genre_id
        self.id = Insert(self).id

    def __iter__(self):
        yield("venue_id", self.venue_id)
        yield("genre_id", self.genre_id)

if __name__=="__main__":
    global_obj = ThinData()
    cli_ctl = CliCtl()