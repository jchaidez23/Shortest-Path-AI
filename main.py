import sys
import math
import heapq
#Jose Acosta
#Use a priority Queue


#Haversine Formula: Calculates the straight line distance between two cities using their longitude and latitude
def haversine(latitude1,latitude2,longitude1,longitude2):
	EARTHRADIUS = 3958.8
	totalLat = (latitude2 - latitude1)/2
	totalLong = (longitude2 - longitude1)/2
	inside = math.sin(totalLat) ** 2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(totalLong) ** 2
	distance = 2 * EARTHRADIUS * math.asin(inside)
	return distance

def astar(city1,city2):
	#Parses through the coordinates.txt file and creates a dictionary which holds the longitude and latitude of the given city acting as the key
	cityCoordinates = {}
	with open('coordinates.txt','r') as file:
		for line in file:
			#strips the string of the unnecessary characters
			(key,val) = line.replace('(','').replace(')','').strip().split(":")
			#creates a tuple of floats by splitting the string
			lat,lon = map(float,val.split(','))
			cityCoordinates[key] = (lat,lon)

	
	with open('map.txt','r') as file:
		locations = {}
		keys = []
		for line in file:
			(key,val) = line.split("-")
			locations[key] = list(val.split(",")) 
			keys.append(key)
		
		for key in locations:
			for i, place in enumerate(locations[key]):
				place = place.split("(")
				place[1] = float(place[1].replace(")",""))
				locations[key][i] = place
	#print(cityCoordinates)
	#print()
	#print(locations)

	start = city1
	goal = city2
	prio_queue = [(0,start)]
	previous_city = {}

	#creates a dictionary of "g" values for f = g+h
	g_values = {}
	#initially infinite and 0 to get accurate readings
	for city in locations:
		g_values[city] = float('inf')
	g_values[start] = 0

	#based off slides from class and changes to greedy algorithm
	while prio_queue:

		x, current = heapq.heappop(prio_queue)

		#checks if the current city is the goal city to create the path
		if current == goal:
			path = []
			while current:
				path.append(current)
				current = previous_city.get(current)
				
            
			return path[::-1]
		#actual algorithm, iterates through locations to get the lowest cost
		for city, distance in locations.get(current):
			g_value = g_values[current] + distance
		#if it finds a cheaper path it puts it on the heap  
			if g_value < g_values[city]:
				previous_city[city] = current
				g_values[city] = g_value
				#* unpacks the tuples for haversine formula and adds it to gvalue
				f_value = g_value + haversine(*cityCoordinates[city], *cityCoordinates[goal])
				#adds it to priority queue with fvalue as its priority
				heapq.heappush(prio_queue, (f_value,city))

			
	
			
if(len(sys.argv) < 2):
	print("Two cities required for program to run")
city1 = sys.argv[1]
city2 = sys.argv[2]
#function = currentcost + straightlinecost
#city1 = "Monterey"
#city2 = "Eureka"
path = astar(city1,city2)
#print(path)
#Converts route to a string to add cities to it
print("From City: ", city1)
print("To City: ", city2)

#after finding optimal route calculates the distance
distance = 0
map = open('map.txt','r')
locations = {}
keys = []
#converts map into a dictionary
for lines in map:
	(key,val) = lines.split("-")
	locations[key] = list(val.split(",")) 
	keys.append(key)
	
for key in locations:
	for i, place in enumerate(locations[key]):
		place = place.split("(")
		place[1] = float(place[1].replace(")",""))
		locations[key][i] = place
#sets distance to 0
distance = 0
#creates a visited list to not double count cities
visited = []
#iterates through the path and gets neigboring cities
for city in path:
	available_cities = {}
	available_cities.update(locations.get(city))
	#checks if city is in dictionary and gets it distance
	#if it was visited does not add anythng and only adds non-visited
	for key in available_cities.keys():
		if key in path:
			visited.append(city)
			if key in visited:
				pass
			else:
				distance+= available_cities.get(key)
	#print(available_cities)
	
#converts path list to a string
#removes city 1 and 2 for ease of printing
path_string = ""
path.remove(city1)
path.remove(city2)
for city in path:
	path_string = path_string + city + " - "

print(city1, " - ", path_string, city2)
print(f"Total Distance: {distance:.2f} mi")