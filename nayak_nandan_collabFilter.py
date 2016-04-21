#import modules
import math
import sys


#arguments
txtfile=sys.argv[1]
userName=sys.argv[2]
n=int(sys.argv[3])
k=int(sys.argv[4])


#global variables
uIndex=0
urIndex=1
movieIndex=2
Print=False


#define functions
def setPrint():
    global Print
    Print=True

def resetPrint():
    global Print
    Print=False


def getUserRatings(myList):
    tempDict={}
    for eachList in myList:
        movie=eachList[movieIndex]
        user=eachList[uIndex]
        userRating=eachList[urIndex]
        if movie in tempDict:
            tempDict[movie][user]=float(userRating)
        else:
            #tempDict[movie][user]=userRating
            tempDict[movie]={}
            tempDict[movie][user]=float(userRating)
        
    return tempDict

def getItemsList(myList):
    tempList=[]
    for eachList in myList:
        movie=eachList[movieIndex]        
        if movie not in tempList:
            tempList.append(movie)
    tempList.sort()
    return tempList

def getUnratedMovies(user,iList,mDict):
    tempDict={}
    tempDict[user]=[]
    userList=[]
    for eachMovie in mDict:        
        if user not in mDict[eachMovie]:            
            tempDict[user].append(eachMovie)
    tempDict[user].sort()
    return tempDict

def getCommonUsers(dict1,dict2):
    tempList=[]
    for key in dict1:
        if key in dict2:
           tempList.append(key)    
    return tempList

def getAvg(myList,myDict):
    total=0
    if len(myList)==0:
        return 0
    for user in myList:
        total+=myDict[user]
        
    mean=float(total)/float(len(myList))        
    return mean
        
    

#Main Function
if __name__=="__main__":
    ratingsFile=open(txtfile,"r+") #Read the .tsv and create a list of lists for each line
    lines=ratingsFile.read()
    lines=lines.split('\n')
    linesList=[]
    for eachItem in lines:
        eachItem=eachItem.split('\t')
        if eachItem!=['']:
            linesList.append(eachItem)


#Create a Dictionary in the format - 
#moviesDict{
#	movie1:{
#		user1:Rating1,
#		user2:Rating2....}
#	movie2:{
#		user1:Rating1,
#		user2:Rating2....}
    moviesDict=getUserRatings(linesList) 
    if Print==True:
        print moviesDict


    unratedMoviesDict={}
    itemsList=getItemsList(linesList) #List of all the unique movies in the given .tsv
#Dictionary of all the unrated movies by a user(passed as argv)
#unratedMoviesDict={User:[movie1,movie2...]}
    unratedMoviesDict=getUnratedMovies(userName,itemsList,moviesDict) 

#Calculating the pearson correlation
    W={}
    for movie in unratedMoviesDict[userName]:
        W[movie]={}
    for urMovie in W:
        for movie in moviesDict:
            if movie!=urMovie:
                commonUsersList=getCommonUsers(moviesDict[urMovie],moviesDict[movie]) #Get the list of co-rated users for unrated movie, rated movie pair              
                avgURMovie=getAvg(commonUsersList,moviesDict[urMovie]) #Average rating of unrated movie
                avgRMovie=getAvg(commonUsersList,moviesDict[movie]) #Average rating of rated movie
                Nr=Dr=term1=term2=0
				
#Nr=summation of [Ru,i - Avg(R)] * [Ru,j - Avg(R)]
#term1 = Square root of summation of [Ru,i - Avg(R)]^2
#term1 = Square root of summation of [Ru,j - Avg(R)]^2
#Dr=term1 * term2
#Pearson correlation= Nr/Dr
                for user in commonUsersList:
                    Nr+=(moviesDict[urMovie][user]-avgURMovie)* (moviesDict[movie][user]-avgRMovie) #Nr=Numerator
                    term1+=(moviesDict[urMovie][user]-avgURMovie)**2                    
                    term2+=(moviesDict[movie][user]-avgRMovie)**2
                term1=math.sqrt(term1)
                term2=math.sqrt(term2)
                Dr=term1*term2 #Dr=Denominator
                if Dr!=0:
                    val=Nr/Dr
                else:
                    val=0
                W[urMovie][movie]=val
    if Print==True:
        print "W"

    
    newDict={}
    for urMovie in W:
        tempList=[]        
        d=W[urMovie]
#Sort all the values in dictionary in descending order. If the values are same, then sort ther keys in alphabetical order
        tempList=[v[0] for v in sorted(d.iteritems(), key=lambda(k, v): (-v, k))]
        newDict[urMovie]=tempList
    
    if Print==True:
        print "NewDict"


#Make prediction for movies with highest pearson correlation for the given user		
    predictionDict={}    
    for urMovie in newDict:
        Nr=Dr=0.00000
        m=n        
        if len(newDict[urMovie]) < n:
            m=len(newDict[urMovie])        
        i=0
        while i<m:
            rMovie=newDict[urMovie][i]
            if userName in moviesDict[rMovie]:
#Nr=Summation of Ru,n * Wi,n
#Dr=Summation of Wi,n
#Prediction for user u for item i = Nr/Dr
                Nr+=W[urMovie][rMovie]*moviesDict[rMovie][userName]
                Dr+=W[urMovie][rMovie]
            else:
                m=m+1
            i+=1
        if Dr!=0:   
            predictionDict[urMovie]=float(Nr)/float(Dr)
        else:
            predictionDict[urMovie]=0.0

#Sort all the values in dictionary in descending order. If the values are same, then sort ther keys in alphabetical order            
    tempList=sorted(predictionDict.items(),key=lambda(k,v):(-v,k))    
    for i in range(k):
        movie=tempList[i]        
        print "%s %.5f"%(movie[0],movie[1])   
    
       
#close all files  
    ratingsFile.close()
   
