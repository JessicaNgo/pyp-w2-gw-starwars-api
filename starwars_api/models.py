from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError
#I am adding the line below


api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        print json_data
        for key, value in json_data.iteritems():
            setattr(self, key, value)
            
            
        
        
        #so if json_data = {'people': 'luke'}, this allows for BaseModel.people = 'luke'?
        #Maybe I am not understanding then; are we creating a dictionary?
        #In my mind, the two ways to approach this are to iterate through everything
        # and pull what we need or make a way to reference back to the AGI every time
        # my impression was the latter, but I make more than my share of mistakes
        # i have absolutely no idea lol

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        #gets called like luke= People.get(1)
        #creates an object named luke with all attributes    
        
        method = "get_{}".format(cls.RESOURCE_NAME)
        retrieved_data = getattr(api_client, method)(people_id = resource_id)
        retrieved_data = BaseModel(retrieved_data)
        # for key, value in retrieved_data:
        #     setattr(self, key, value)
        print retrieved_data
        return retrieved_data #returns loaded python object from json file
        

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        #call on base queryset...? instance an object
        modelqueryset = "{}QuerySet".format(cls.__name__)
        eval(modelqueryset)
        

class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        
        pass
    

    def __iter__(self):
        #initializing 
        
        self.index = 0
        self.current_page = 1
        #self.total_page = 1
        #loading in one page at a time, initialize first page
        self.curr_page_results = getattr(api_client, method)(page = current_page)
    
        return self

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        method = "get_{}".format(self.RESOURCE_NAME)
        
        #check pagelength
        self.pagelength = len(self.results)
        
        #iterate through results on page
        while self.index <= self.pagelength:
            yield self.results[self.index]
            self.index +=1
            
        #go to next page
        self.current_page += 1
        
        #check for next page exists, if it does, reset index & load next page
        if getattr(api_client, method)(page = self.current_page):
            self.curr_page_results = getattr(api_client, method)(page = current_page)
            self.index = 0
            #self.total_page += 1
            #theoretically can enter while loop again?
        else: #page does not exist
            raise StopIteration
        
    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        if self.count:
            return self.count #'count' key contains total entries
        else:
            method = "get_{}".format(self.RESOURCE_NAME)
            retrieved_data = getattr(self, method)()
            return retrieved_data["count"]
            
            #manually count


class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))
