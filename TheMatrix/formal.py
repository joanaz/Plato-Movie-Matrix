import sys, os                                                                                                                                                                                  
sys.path.append('/root/TheMatrix/TheMatrix/TheMatrix')                                                                                                                                          
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'                                                                                                                                              
from django.conf import settings    
from Plato.models import *
from pymongo import MongoClient
from textblob import TextBlob

#import Plato.models

client = MongoClient()                                                                                                                                                                       
db = client.plato_test                                                                                                                                                                      
collection = db.review                                                                                                                                                                      
theList = []

def loadPerception():                                                                                                                                                                          
    presentTotal = 0
    presentPol = 0
    presentSub = 0
    count = 1
    # Have dictionary keep track of duplicates. skip them if dup.                                                 
    dupCheck = set([])    
    movCheck = set([])

    Percy = collection.find(no_cursor_timeout=True)
    for review in Percy:
        if (review["user_id"] in dupCheck):
            continue
        else:
            dupCheck.add(review["user_id"])
            userID = review["user_id"]
            snake = collection.find({"user_id":userID}) 
            #bob = snake.sort("time")
            
            for ele in snake:
                if (ele["movie_id"] in movCheck):
                    continue
                else:
                    movCheck.add(ele["movie_id"])
                    print "added"
                    sum_text = ele["summary"]                                                                                                                                                   
                    text =  ele["full_text"]                                                                                                                                                 
                    blob = TextBlob(text)                                                                                                                          
                    sumBlob = TextBlob(sum_text)  


                    presentTotal += ele["score"]                                                                                                                               
                    presentPol += sumBlob.sentiment.polarity
                    presentSub += sumBlob.sentiment.subjectivity

                    presentAvg = presentTotal/count
                    presentPAvg = presentPol/count
                    presentSAvg = presentSub/count
    
                    entry = unitPerception(movie_id=ele["movie_id"],score = ele["score"], adjustedScore = ele["score"])                                                                
                    theList.append(entry)                                                                                                                         
                    count +=1 
                        
            if avg_polarity != 0:
                perceptionEntry = Perception(user_id = userID, avg_polarity= presentPAvg, avg_subjectivity= presentSAvg, avg_score = presentAvg,elements = theList)       
                perceptionEntry.save()                                                                                                                                                             
            theList = []                                                                                                                                                                        
            count = 1                                                                                                                                                                           
            presentTotal = 0
            presentPol = 0
            presentSub = 0

def loadAnchoring():
    presentTotal = 0
    count = 1
    # Have dictionary keep track of duplicates. skip them if dup. up count until get at least 10 unique
    dupCheck = set([])

    Bob = collection.find(no_cursor_timeout=True)#.limit(10000)

    for review in Bob:
        if (review["movie_id"] in dupCheck):
            continue
        else:
            dupCheck.add(review["movie_id"])
            movieID = review["movie_id"] 
            snake = collection.find({"movie_id": movieID})#.distinct("time") 
            if snake.count() < 100:
                print("Skipped")
                continue
            else:
                print ("GO!")
                bob = snake.sort("time")     
                for ele in bob:
                    presentTotal += ele["score"]
                    presentAvg = presentTotal/count
                    
                    entry = unitAnchoring(time = ele["time"], present_avg_score = presentAvg, most_recent_ind_score = ele["score"])
                    theList.append(entry)
                    count +=1
        
                anchorEntry = Anchoring(movie_id = movieID, elements = theList)
                anchorEntry.save()
                theList = []
                count = 1
                presentTotal = 0

def loadRicher():
    presentTotal = 0
    helpfulNum = 0
    helpfulDen = 0
    count = 1                                                                                                                                                                                   
    # Have dictionary keep track of duplicates. skip them if dup. up count until get at least 10 unique                                                                                         
    dupCheck = set([]) 
    movCheck = set([])
    Richie = collection.find(no_cursor_timeout=True)
    for review in Richie:                                                                                                                                                                       
        if (review["user_id"] in dupCheck):                                                                                                                                                     
            continue                                                                                                                                                                            
        else:
            dupCheck.add(review["user_id"])                                                                                                                                                     
            userID = review["user_id"]                                                                                                                                                          
            snake = collection.find({"user_id":userID})                                                                                                                                         
            presentTotal = snake.count()
            for ele in snake:                                                                                                                                                                   
                if (ele["movie_id"] in movCheck):                                                                                                                                               
                    continue                                                                                                                                                                    
                else:                                                                                                                                                                           
                    movCheck.add(ele["movie_id"])         
                    helpfulNum += int((str.split(ele["helpfulness"].encode('ascii','ignore'), "/"))[0])
                    helpfulDen += int((str.split(ele["helpfulness"].encode('ascii','ignore'), "/"))[1])
                count += 1
            entry = bestHuman(user_id = ele["user_id"],numMovies = presentTotal, mostHelped=helpfulNum, totalHelped=helpfulDen) 
            entry.save()
            count = 1
            helpfulNum = 0
            helpfulDen = 0
            print "added"
if __name__ == "__main__":                                                                                                                                                                     
    print "Beginning upload"                                                                                                                                                                    
    #query()
    #other()
    #sentiment()
#    loadPerception()
    loadRicher()
# **** REAL THINGS
#    loadAnchoring()
