"""
Name: Nicholas Miller
Description: tools for working with Yelp Dataset Challenge JSON files
Bugs: Parsing the reviews file is very slow; optimization needed
"""

import json
import pickle

#replace this with the directory of your business JSON file

yelp_path = '../../yelp/yelp_dataset_challenge_round9/'

business_path = yelp_path + 'yelp_academic_dataset_business.json'

#replace this with the directory of your review JSON file
review_path = yelp_path + 'yelp_academic_dataset_review.json'

class YelpParser:
    def __init__(self, source_path):
        self.source = source_path

class BusinessParser(YelpParser):
    """Class for parsing JSON of Yelp businesses"""
    def __init__(self, source_path):
        YelpParser.__init__(self, source_path)

    def find_matching_categories(self, match_string):
        """Find businesses in JSON having at least one category matching the match_string"""
        #input: list of lines of Yelp business info, each a JSON object
        #Note: I did readlines() instead of json.load because it's quite large
        #output: list of JSON lines that include 'match' in category attribute
        
        matches = []
        with open(self.source) as f:
            while f.readline():
                line = f.readline()
                cats = json.loads(line)['categories']
                if cats:
                    for cat in cats: 
                        if match_string in cat:
                            matches.append(line)
        return matches
    
    def get_categories(self):
        """Return dict of all categories in the JSON, with their counts"""
        #Output: a dict of all the categories appearing in the dataset
        category_dict = {}
        with open(self.source) as f:
            while f.readline():
                line = f.readline()
                if json.loads(line)['categories']:
                    for category in json.loads(line)['categories']:
                        category_dict[category] = category_dict.get(category, 0) + 1
        return category_dict 

    def get_ids_for_category(self,  match_string):
        """Return list of all IDs of business having category matching match_string"""
        #input: string to match in category
        #output: list of business IDs
        #note: we use this to search the reviews later
        matches = self.find_matching_categories(match_string)
        return [json.loads(match)['business_id'] for match in matches]
         

class ReviewParser(YelpParser):
    """Class for working with JSON of yelp reviews"""
    def __init__(self, source_path):
        YelpParser.__init__(self, source_path)

    def get_data_from_json(self):
        """Load data from source path as a JSON data object"""
        #Input: JSON file
        #Output: JSON object
        #We don't use loads() because it's dumped as json, not string
        with open(self.source) as f:
            data = json.load(f)        
        return data

    def get_reviews_by_ids(self, ids):
        """Get reviews matching given IDs"""
        #Input: business IDS    
        #output list reviews for given IDs, each as JSON object
        reviews = []
        with open(self.source) as f:
             while f.readline():
                 line_data = json.loads(f.readline())
                 if line_data['business_id']:
                     if line_data['business_id'] in ids:
                         reviews.append(line_data)
        return reviews

    def pickle_reviews(self, reviews, dest):
        #Input: list of Yelp reviews, each as a JSON object, destination file
        #Output: pickle file
        with open(dest, 'wb') as p:
            pickle.dump(reviews, p)

    def write_to_json(self, reviews, dest):
        #Input: list of Yelp reviews, each as  a JSON object
        #output: JSON file
        #Note that it is *not* advisable to do this line by line, you have to dump the whole thing
        with open(dest, 'w') as dest:
             json.dump(reviews, dest, indent=2)

def parser_demo(query):
    #Create BusinessParser object
    #We'll use this to find IDs matching the user's queried category
    bp = BusinessParser(business_path)

    #Find out how many categories there are, just for fun
    categories = bp.get_categories()
    print("Found {0} categories".format(len(categories.keys())))

    #Get categories matching the user's query
    matching_categories = bp.find_matching_categories(query)
    print("Found {0} businesses related to {1}".format(len(matching_categories), query))

    #Get business IDs matching the user's query
    #We'll need these when searching the reviews
    matching_ids = bp.get_ids_for_category(query)
    print("Got ids for {0}".format(query))
    
    #Create ReviewParser object
    #We'll use this to search the reviews
    rp = ReviewParser(review_path)

    #Get reviews of businesses with IDs we found earlier
    matching_reviews = rp. get_reviews_by_ids(matching_ids)
    print("Found {0} reviews for {1} businesses".format(len(matching_reviews), query))

    #Pickle the reviews so they're easier to retrieve later
    pickle_path = query.lower().replace(' ', '_') + '_reviews.pickle'
    rp.pickle_reviews(matching_reviews, pickle_path)
    print("Pickled reviews to {0}".format(pickle_path))

    #Save the reviews to a JSON file
    json_path = query.lower().replace(' ', '_') + '_reviews.json'
    rp.write_to_json(matching_reviews, json_path)
    print("Wrote {0} reviews to {0}".format(query, json_path))

    #Create a JSON data object that we can play with
    mr = ReviewParser(json_path)
    mr_data = mr.get_data_from_json()
    return mr_data

if __name__ == '__main__':
    parser_demo('Travel')
