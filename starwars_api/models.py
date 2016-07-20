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
        
        for key, value in json_data.iteritems():
            setattr(self, key, value)
        
        
        

    @classmethod
    def get(cls, resource_id = 1):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        #gets called like luke= People.get(1)
        #creates an object named luke with all attributes    
        
        method = "get_{}".format(cls.RESOURCE_NAME)
        retrieved_data = getattr(api_client, method)(people_id = resource_id)
        retrieved_data = BaseModel(retrieved_data)

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
        
        #want to execute PeopleQuerySet() - turn into iterable
        
        self = iter(eval(modelqueryset)()) #at this point the class of this is changed to PeopleQuerySet
        self.oldclassname = cls.__name__
        return self

        
        

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


class BaseQuerySet(object): #want next object

    def __init__(self):
        #getattr(api_client, )
        print "entered __init__ of Parent"
        self.method = "get_{}".format(self.RESOURCE_NAME)
        self.retrieved_data = getattr(api_client, self.method)()
        
        

    def __iter__(self): #objects we want are a list of dictionaries inside a dictionary value with key 'results'
        #initializing 
        #print "entered __iter__"
        
        self.index = 0
        self.current_page = 1
        
        
        #loading in one page at a time, initialize first page, page length
        self.curr_page_results = getattr(api_client, self.method)(page = self.current_page)['results']
        self.pagelength = len(self.curr_page_results)
        
        return self
        
    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        self.objects = []
        #check if next page exists
        while self.next:
                
            #iterate through results on page, create object for each
            while self.index < self.pagelength:
                
                created_object = eval(self.oldclassname)(self.curr_page_results[self.index])
                self.index +=1
                self.objects.append(created_object)
                return created_object
                
            #go to next page
            self.current_page += 1
            
            #load next page results
            self.curr_page_results = getattr(api_client, self.method)(page = self.current_page)
            
            #find next page length
            self.pagelength = len(self.curr_page_results)
            
            #reset index
            self.index = 0
            
        
        raise StopIteration
        
    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        # if self.count:
        #     return self.count #'count' key contains total entries
        # else:
        method = "get_{}".format(self.RESOURCE_NAME)
        retrieved_data = getattr(api_client, method)()
        return retrieved_data["count"]
            


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
