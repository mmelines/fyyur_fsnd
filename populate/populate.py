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
    genre_list = [ "Rock", "Folk", "Jazz", "Hip Hop", "Country",
        "Bluegrass", "Pop", "Blues", "Metal", "Prog", "Punk", "Soul", "Funk",
        "Reggae", "Disco", "Electronic", "Indie", "Alt", "Gospel", "Swing",
        "Blues Rock", "Grunge"]
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
            RdDb.location_names and -1
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
        return phone number formatted as a string
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
        generate random specific street address
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

    @classmethod
    def update_loc(self):
        """
        """
        sel = Select()
        for loc in RdDb.location_names:
            location_ids = Select().loc_search(loc)
            RdDb.locations[loc]["venue_ids"] = location_ids[0]
            RdDb.locations[loc]["artist_ids"] = location_ids[1]
        logging.debug("RdDb. returning None (only option)")
        logging.info("RdDb.update_loc completed")

    @staticmethod
    def new_schedule_item():
        # get current time
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
        self.artist_ids = Select().get_entity_ids("artist")
        self.venue_ids = Select().get_entity_ids("venue")
        self.show_ids = Select().get_entity_ids("show")
        self.genres = Select().get_genres()
        self.genre_ids = Select().get_entity_ids("genre")
        self.locations = {}
        self.log_global = 0
        self.model = self.new_singleton()
        logging.info("completed RdDb __init__")

    def log(self, log_type, ftn_name, **kwargs):
        info_msg = "Thindata." + ftn_name
        if log_type == "call":
            info_msg = "called " + msg
        if log_type == "out":
            infog_msg += "completed."
            if ftn_name == "new_singleton":
                debug_msg = "Returning new model"
            if "add" in kwargs.keys():
                 debug_msg += "\nAdded " + kwargs["add"]  
            if "find" in kwargs.keys():
                 debug_msg += "\nFound " + kwargs["find"]
            if "entity_string" in kwargs.keys():
                 debug_msg += "\nUpdated model to include " + kwargs[entity_string] 
            logging.debug(debug_msg)
        logging.info(info_msg)

    def new_singleton(self):
        """
        get all venue and artist ids by location and add them to both:
            - self.locations[location]["venue_ids"] and
                self.locations[location]["artist_ids"]
                (contains only ids for location)
            - self.artist_ids and self.venue_ids (contains all ids)
        """
        def log_singleton(function, *args):
            """
            logging functions for RdDb.new_singleton
            """
            if function == "call":
                msg = "called RdDb.new_singleton()"
                logging.info(msg)
            if function == "summarize" and len(args) == 3:
                data_function = "self.venue_ids is " + str(args[1])
                data_function += "\n  & self.artist_ids is " + str(args[2])
                logging.debug(data_function)
                msg = "Rd.Db.new_singleton completed"
                logging.info(msg)

        log_singleton("call")
        self.model = {}
        self.artists = []
        self.venues = []
        self.shows = []
        self.genres = []
        for location in RdDb.location_names:
            obj = {"venues": {},
                    "venue_ids": [],
                    "artists": {},
                    "artist_ids": [],
                    "shows": []}
            ids = Select().loc_search(location)
            # add venue info to each location
            for item in ids[0]:
                # add item to list of location venue_ids
                obj["venue_ids"].append(item)
                self.venues.append(item)
                # add blank scheduling item to list of location venue_ids
                obj["venues"][item] = {"shows": {}}
                # get show details for every venue in the specified area
                venue_shows = Select().get_venue_shows(item)
                # if the query returns a result, add: 
                #  - a show id to self.venue_shows
                if not venue_shows is None:
                    # add show_ids to obj["shows"] if it's not there already
                    for show_id in venue_shows:
                        # add start date listing as the key
                        # obj["venues"][item][]
                        if not show_id in obj["shows"]:
                            obj["shows"].append(show_id)
                        if not show_id in self.shows:
                            self.shows.append(show_id)
            # add artist info to each location !!TODO
            for item in ids[1]:
                obj["artist_ids"].append(item)
                if not item in self.artists:
                    self.artists.append(item)
                obj["artists"][item] = {"shows": {}}
                artist_shows = Select().get_artist_shows(item)
                if not artist_shows is None:
                    # add show_ids to obj["shows"] if it's not there already
                    #    continues 
                    for show_id in artist_shows:
                        if not show_id in obj["shows"]:
                            obj["shows"].append(show_id)
                        if not show_id in self.shows:
                            self.shows.append(show_id)
            for item in obj["shows"]:
                dtl = Select().get_show_detail(item)
                if not dtl == []:
                    # if show_id isn't already in the location show obj, add:
                    #   - the show id to to obj[<entity_type>s][<id>][show_ids]
                    #   - the detailed scheduling object to blank space created
                    #       in obj[<entity_type>s][<id>] with key [start_time]
                    show_obj = {"venue_id": dtl[0],
                            "artist_id": dtl[1],
                            "start_time": dtl[2],
                            "end_time": dtl[3],
                            "show_id": item}
                    same_day = True
                    if dtl[3].day != dtl[2].day:
                        same_day = False
                        second_start = datetime.datetime(dtl[3].year,
                                                            dtl[3].month,
                                                            dtl[3].day,
                                                            1, 0, 0)
                    if not item in obj["artists"][dtl[1]]["shows"].keys():
                        obj["artists"][dtl[1]]["shows"][item] = dtl[2]
                        obj["artists"][dtl[1]]["shows"][dtl[2]] = show_obj
                        if not same_day:
                            obj["artists"][dtl[1]][second_start] = show_obj
                    if not item in obj["venues"][dtl[0]]["shows"].keys():
                        obj["venues"][dtl[0]]["shows"][item] = dtl[2]
                        obj["venues"][dtl[0]]["shows"][dtl[2]] = show_obj
                        if not same_day:
                            obj["venues"][dtl[0]][second_start] = show_obj
            self.model[location] = obj
        self.model["artists"] = self.artists
        self.model["venues"] = self.venues
        self.model["shows"] = self.shows
        self.model["genres"] = {}
        log_singleton("summarize", self.venue_ids, self.artist_ids)
        return self.model

    def __repr__(self):
        """
        represent data in RdDb class instance
        """
        msg = "\n" + "-" * 30 + "\n" + str(self.model)
        msg += "(global) RdDb (random data) item: "
        msg += "\n   - artist_ids: " + str(self.artist_ids) 
        msg += "\n   - venue_ids: " + str(self.venue_ids)
        msg += "\n   - show_ids: " + str(self.show_ids)
        msg += "\n   - genre_ids: " + str(self.genre_ids)
        msg += "\n" + "-" * 30 + "\n"
        msg += str(RdDb.locations)
        return msg

    def append_entity(self, ent):
        """
        """
        self.log("call", "append_entity")
        loc = ent.city
        ents = ent.entity_type + "s"
        ent_ids = ent.entity_type + "_ids"
        ent_str = ""
        if ent.entity_type in ["artist", "venue"]:
            ent_str += ent.entity_type[0] + str(ent.id)
            # add entity_id to local <entity_type>_ids list
            if ent.id not in self.model[loc][ent_ids]:
                self.model[loc][ent_ids].append(ent.id)
            # add entity_id key & blank dict to local <entity_type>s dict
            if ent.id not in self.model[loc][ents]:
                self.model[loc][ents][ent.id] = {}
            # add entity_id to global <entity_type>s list
            if ent.id not in self.model[ents]:
                self.model[ents].append(ent.id)
            # add entity_id to global self.<entity_type>_ids obj
            if ent.entity_type == "artist" and ent.id not in self.artists:
                self.artists.append(ent.id)
            elif ent.entity_type == "venue" and ent.id not in self.venues:
                self.venues.append(ent.id)
        elif ent.entity_type == "show":
            ent_str += "s" + str(ent.id)
            # add entity_id to local show_ids list
            if ent.id not in self.model[loc]["show_ids"]:
                self.model[loc]["show_ids"].append(ent.id)
                # add entity_id to local <entity_type>s dict for show, venue
                show_obj = {"venue_id": ent.venue_id,
                            "artist_id": ent.artist_id,
                            "start_time": ent.start_time,
                            "end_time": ent.end_time,
                            "show_id": ent.id}
                if ent.id not in self.model[loc]["artists"][ent.artist_id].keys():
                    self.model[loc]["artists"][ent.artist_id][ent.id] = show_obj
                if ent.id not in self.model[loc]["venues"][ent.venue_id].keys():
                    self.model[loc]["venues"][ent.venue_id][ent.id] = show_obj
            # add entity_id to global shows list
            if ent.id not in self.model["shows"]:
                self.model["shows"].append(ent.id)
            # add entity_id to global self.show_ids
            if ent.id not in self.shows:
                self.shows.append(ent.id)
        self.log_global += 1
        self.log("out", "append_entity", entity_string=ent_str)

    def new_genre(self, genre_name):
        """
        add unique genre to RdDb.genre_ids
        """
        self.log("call", "new_genre")
        if self.genres is None:
            self.genres = []
        if not genre_name in self.genres:
            #find id genre_name in genres database
            result = Select().verify_genre(genre_name)
            # if genre_name doesn't exist in the database, add it
            if result == False or result == -1:
                new_genre = Genre(genre_name)
                self.genre_ids.append(new_genre.id)
                self.genres.append(new_genre.name)
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
        self.new_artists = 0
        self.new_venues = 0
        self.new_shows = 0
        self.clear_db(True)
        self.commit_genres()
        self.gen_entities(self.entity_prompt())
        logging.info("completed .__init__")
        for ent in self.new_values:
            ent.__repr__()
        pprint(global_obj.model)

    def __repr__():
        msg = "CLI CTL\n" + str(self.ent)
        msg += "*"*20
        msg += "\n\n***\nnew genres: " + str(self.new_genres)
        msg += "\n\n***\nnew artists: " + str(self.new_artists)
        msg += "\n\n***\nnew venues: " + str(self.new_venues)
        msg += "\n\n***\nnew shows: " + str(self.new_shows)
        return msg
    
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

    def entity_prompt(self):
        """
        diplays cli input menu to get number of entities to create
        """
        logging.info("called CliCtl.entity_prompt")
        prompt = "\nEnter number of %s entities to create now:\n(%s already"
        prompt += " exist)"
        confirm_zero = "\nNo new %ss will be created"
        print("# artists: " + str(len(global_obj.model["artists"])))
        print("# venues: " + str(len(global_obj.model["venues"])))
        print("# shows: " + str(len(global_obj.model["shows"])))
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
            new_values = []
            while new_entities < goal and backup_count < goal * 5:
                if ent_type == "artist":
                    ent = Artist()
                    ent.__repr__()
                if ent_type == "venue":
                    ent = Venue()
                    ent.__repr__()
                print(ent_type + "id is " + str(ent.id))
                if isinstance(ent.id, int) and ent.id > 0:
                    new_entities += 1
                    global_obj.append_entity(ent)
                    self.new_values.append(ent)
                backup_count += 1
            if new_entities >= goal:
                success = True
            global_obj.model[("new_" + ent_type + "s")] = new_values
            return success

        logging.info("called CliCtl.gen_entities")
        print("gen_entities sees " + str(entities))
        msg = "Generating "
        msg += str(entities[0]) + " Artist entities"
        msg += ", " + str(entities[1]) + " Venue entities"
        msg += ", " + str(entities[2]) + " Show entities."
        print(msg)
        loop_control = True
        if entities[0] > 0:
            loop_control = match_count(entities[0], "artist")
            if loop_control:
                self.new_artists += entities[0]
        if entities[1] > 0 and loop_control:
            loop_control = match_count(entities[1], "venue")
            if loop_control:
                self.new_venues += entities[1]
        if entities[2] > 0 and loop_control:
            for artist in global_obj.model["artists"]:
                self.make_shows("artist", artist, entities[2])
            for venue in global_obj.model["venues"]:
                self.make_shows("venue", venue, entities[2])
        logging.debug("CliCtl.gen_entities returning None (default)")
        logging.info("CliCtl.gen_entities completed")

    def make_shows(self, entity_type, entity_id, amount):
        print("makes_shows config for show for " + entity_type + " # " + str(entity_id))
        number = self.decide_amount(amount)
        new_shows = 0
        backup_counter = 0
        try:
            if entity_type == "venue":
                existing = len(Select().get_venue_shows(venue_id))
            if entity_type == "artist":
                existing = len(Select())
        except:
            existing = 0
        finally:
            if existing < number:
                new_shows = existing
                while new_shows <= number and backup_counter <= (number * 3):
                    show = None
                    if entity_type == "artist":
                        show = Show(artist_id=entity_id)
                    if entity_type == "venue":
                        show = Show(venue_id=entity_id)
                    if not show is None and isinstance(show.id, int):
                        if show.id > 0:
                            new_shows += 1
                            global_obj.append_entity(show)
                            self.new_values.append(show)
                    backup_counter += 1

    def decide_amount(self, amount):
        amount_top = amount + 4
        if (amount - 4) < 3:
            amount_bottom = 3
        else:
            amount_bottom = amount-4
        amount = random.choice(range(amount_bottom, amount_top))
        return amount

    @staticmethod
    def clear_db(confirm):
        """
        """
        def confirm_confirm():
            msg_prompt = "\nthis run will delete all existing dbentities and "
            msg_prompt += "re-randomize the db from scratch.\nAre you sure you "
            msg_prompt += "want to do this?"
            print(msg_prompt)
            answer = input(">> Y/n: ")
            valid_answer = False
            backup_count = 0
            while valid_answer == False and backup_count <= 10:
                answer = answer.strip()
                answer = answer.lower()
                if answer in ["y", "yes", "n", "no"]:
                    print("answer is valid.")
                    valid_answer = True
                    if answer[0] == "y":
                        print("answer was yes.")
                        decision = True
                    if answer[0] == "n":
                        print("answer was no.")
                        decision = False
                else:
                    backup_count += 1
                    msg_remind = "\n\n" + answer + "is an Invalid response. "
                    msg_remind += "Please enter YES or NO"
                    if backup_count == 10:
                        msg = "\nI didn't understand your responses. Existing "
                        msg += "data will not be altered."
                        print(msg)
                    decision = False
            return decision

        if confirm == True:
            confirm = confirm_confirm()
        if confirm == True:
            successes = 0
            for entity in ["show", "artist", "venue", "genre"]:
                query = "DELETE FROM " + entity + ";"
                result = DbData("delete", query)
                if result == "success":
                    successes += 1
            msg = "successfully deleted "
            if successes == 4:
                msg += "all existing entities"
            elif successes > 0:
                msg += str(successes) + " entities; error in DbData.delete()"
            else:
                msg += "nothing. error in DbData.delete()"
            global_obj.model = global_obj.new_singleton()
        else: 
            print("this run will create additional records w/o clearing db")

    def commit_genres(self):
        for genre_name in RdDb.genre_list:
            genre_id = None
            backup_count = 0
            while genre_id is None and backup_count < 10:
                genre = Genre(genre_name)
                genre_id = genre.id
                backup_count += 1
            if not genre_id is None:
                global_obj.model["genres"][genre_name] = genre_id
                self.new_values.append("g" + str(genre_id))
                self.new_genres += 1

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
            if args[0] == "insert":
                self.ins_query(args[1])
                self.result = self.__repr__()
                self.make()
            if args[0] == "delete":
                self.query = args[1]
                self.result = self.delete(self.query)
        logging.info("completed DbData.__init__")

    def err(self, err, exc_info, msg):
        """
        """
        self.status = -1
        self.error = {"info": exc_info[1],
                    "msg": msg}
        if not err is None:
            self.error["psycopg2_error"] = '{}'.format(err)
        print(self.error)
        logging.error(self.error)
        self.result = False
        return err

    def delete(self, query):
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
        repr_iter = [
            ["active", "default" if not hasattr(self, "active") else str(self.active)],
            ["error", "default" if not hasattr(self, "error") else str(self.error)],
            ["status", "default" if not hasattr(self, "status") else str(self.status)],
            ["result", "default" if not hasattr(self, "result") else str(self.result)],
            ["value_list", "default" if not hasattr(self, "value_list") else str(self.value_list)],
            ["class_name", "default" if not hasattr(self, "class_name") else str(self.class_name)],
            ["query", "default" if not hasattr(self, "query") else str(self.query)]]

        msg = "\n=========== "
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
        accepts args in [logging_type, ftn_name, class_name]
         - log_type: can be "call", "output" or None type
         - ftn_name: name of class function from which log was called
         - kwargs: lists objects updated or returned by function
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
            summary += "\n                - query: " + self.query
        else:
            summary += "\n                - query: none."
        if hasattr(self, "result"):
            summary += "\n                - attributes: " + str(self.value_list)
        else:
            summary += "\n                - attributes: none."
        if hasattr(self, "value_list"):
            summary += "\n                - result: " + str(self.result)
        else:
            summary += "\n                - result: none."
        summary += "\n                - status: " + str(self.status)
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
        logging.debug("DbData.get_entity returning 'tuple': " + str((query, [ent.name, ent.phone], ent.entity_type)))
        logging.info("completed DbData.")
        return (query, [ent.name, ent.phone], ent.entity_type)       

class Select(DbData):
    """
    functions and methods for db selects
            active
            error
            status
            result
            res_list
            value_list
            class_name
            query
            id
    """

    def __init__(self):
        """
        init object of class select query
        generate queries based on specific needs for selecting automatically
          generated entities
        """
        super().__init__("select")
        self.id = self.result if isinstance(self.result, int) and self.id > 0 else -1
        logging.info("completed Select.__init__")

    def get_entity_ids(self, entity_name):
        """
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
        returns location string for venue or artist id if it is a default location
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

    def count_shows(self, artist_id):
        """
        return # of shows already present in database for artist id
        """
        self.log("call", "count_shows", id=artist_id)
        self.query = "SELECT COUNT id FROM show WHERE id=%s;"
        self.value_list = [artist_id]
        result = self.get()
        if not result is None and result > 0 :
            self.result = result
        self.log_return("count_shows", count=self.result)
        self.log("out", "count_shows")
        return self.result

    def get_show_detail(self, show_id):
        """

        """
        self.log("call", "get_show_detail", show_id=show_id)
        self.query = "SELECT venue_id, artist_id, start_time, end_time FROM "
        self.query += " show WHERE id=%s;"
        self.value_list = [show_id]
        result = self.get()
        return result

    def verify_genre(self, genre_name):
        self.log("call", "verify_genre")
        self.query = "SELECT id FROM genre WHERE name=%s;"
        self.value_list = [genre_name]
        self.result = self.get()
        self.log_return("verify_genre", genre_id=self.result)
        self.log("out", "verify_genre")
        return self.result

    def get_genre(self, genre_id):
        """
        get name of genre from genre table
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
        DbData.__init__(self, "insert", entity)
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
        self.has_image = True
        self.is_seeking = random.choice([True, False])
        logging.info("completed Entity.__init__")

    def log(self, log_type, ftn_name, **kwargs):
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
        yield ("genre_list", self.genre_list)
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
        logging.debug("called Venue.__init__")

    def __repr__(self):
        """
        Display attributes generated for Venue object
        """
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
        yield ("genre_list", self.genre_list)
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
        self.address = None
        self.name = None
        self.facebook_link = None
        self.website_link = None
        self.seeking_description = None
        self.image_link = None
        self.id = None
        init_control = True
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
        yield ("venue_id", self.venue_id)
        yield ("artist_id", self.artist_id)
        yield ("start_time", self.start_time)
        yield ("end_time", self.end_time)
        yield ("all_day", self.all_day)

    def log(self, log_type, ftn_name, *args):
        info_msg = "Show." + ftn_name
        if log_type == "call":
            info_msg = "Called " + info_msg
        if log_type == "init":
            debug_msg = "init control is "
            if len(args) >= 1:
                debug_msg += str(args[0]) + " following " + ftn_name
            logging.debug(debug_msg)
        if log_type == "out":
            info_msg += " completed."
        logging.info(info_msg)

    def set_given_ids(self, kwargs):
        self.init_control = True
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
        self.log("init", "set_given_ids", self.init_control)
        return self.init_control

    def get_other_id(self):
        init_control = True
        if hasattr(self, "city") and self.city is None:
            return False
        if self.init_type == "venue":
            pair_id = None
            if len(global_obj.model[self.city]["artist_ids"]) > 0:
                pair_id = random.choice(global_obj.model[self.city]["artist_ids"])
                self.artist_id = pair_id
            if not isinstance(pair_id, int):
                pair_id = Artist(self.city).id
        elif self.init_type == "artist":
            pair_id = None
            if len(global_obj.model[self.city]["venue_ids"]) > 0:
                pair_id = random.choice(global_obj.model[self.city]["venue_ids"])
                self.venue_id = pair_id
            if not isinstance(pair_id, int):
                pair_id = Venue(self.city).id
        elif self.init_type == "dual":
            pair_id = 0
        else:
            init_control = False
        if pair_id is None or not isinstance(pair_id, int):
            init_control = False
        if not isinstance(pair_id, int):
            init_control = False
        self.log("init", "get_other_id", self.init_control)
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
        self.log("init", "get_location", self.init_control)
        return success

    def schedule(self):
        dates = RdDb.new_schedule_item()
        self.start_time = dates[0]
        self.end_time = dates[0]
        self.log("init", "schedule", self.init_control)
        return True

# --- Genre entity object class -----------------------------------------------

class Genre(DbData):
    """
    stores variables and functions to keep Genre function updated
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
            if isinstance(args[0], int):
                self.copy()
        logging.info("completed Genre.__init__")

    def __iter__(self):
        yield ("name", self.name)

    def copy(self, genre_id):
        name = Select().get_genre(genre_id)
        if not name is None:
            self.name = name
        self.id = genre_id

global_obj = ThinData()

if __name__=="__main__":
    cli_ctl = CliCtl()
    print(cli_ctl).__repr__()