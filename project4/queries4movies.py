from neo4j.v1 import GraphDatabase, basic_auth

#connection with authentication
driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "password"), encrypted=False)

#connection without authentication
#driver = GraphDatabase.driver("bolt://localhost", encrypted=False)

session = driver.session()
transaction = session.begin_transaction()

outputStr = ''

# List the first 20 actors in descending order of the number of films they acted in
# OUTPUT: actor_name, number_of_films_acted_in
outputStr += '### Q1 ###\n'
result = transaction.run('MATCH (actor:Actor)-[:ACTS_IN]->(m:Movie) RETURN actor.name, COUNT(m) AS num_of_films_actedIn ORDER BY num_of_films_actedIn DESC LIMIT 20')
for record in result:
    outputStr += record['actor.name'] + ', ' + str(record['num_of_films_actedIn']) + '\n'
outputStr += '\n'

# List the titles of all movies with a review with at most 3 stars.
# OUTPUT: movie title
outputStr += '### Q2 ###\n'
result = transaction.run('MATCH (p:Person)-[r:RATED]->(m:Movie) WHERE r.stars <= 3  RETURN m.title')
for record in result:
    outputStr += record['m.title'] + '\n'
outputStr += '\n'

# List the titles of all movies with a review with at most 3 stars.
# OUTPUT: movie title
outputStr += '### Q3 ###\n'
result = transaction.run('MATCH (actor:Actor)-[:ACTS_IN]->(m:Movie)<-[r:RATED]-(:Person) WHERE r.stars >= 0 RETURN m.title, COUNT(actor) as numCasts ORDER BY numCasts DESC LIMIT 1')
for record in result:
    outputStr += record['m.title'] + ', ' + str(record['numCasts']) + '\n'
outputStr += '\n'

# Find all the actors who have worked with at least 3 different directors (regardless of how many movies they acted in). 
# For example, 3 movies with one director each would satisfy this (provided the directors where different), but also a single movie with 3 directors would satisfy it as well. 
# OUTPUT: actor_name, number_of_directors_he/she_has_worked_with'''
outputStr += '### Q4 ###\n'
result = transaction.run('MATCH ((actor:Actor)-[:ACTS_IN]->(m:Movie)<-[:DIRECTED]-(director:Director)) WITH actor, COUNT(DISTINCT director) AS num_directors WHERE num_directors>= 3 RETURN actor.name, num_directors')
for record in result:
    outputStr += record['actor.name'] + ', ' + str(record['num_directors']) + '\n'
outputStr += '\n'

# The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the "co-acting" graph.
# That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1;
# All actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc.
# List all actors whose Bacon number is exactly 2 (first name, last name). You can familiarize yourself with the concept, by visiting The Oracle of Bacon.
# OUTPUT: actor_name
outputStr += '### Q5 ###\n'
result = transaction.run('MATCH (bacon2:Actor)-[:ACTS_IN]->(m2:Movie)<-[:ACTS_IN]-(bacon1:Actor)-[:ACTS_IN]->(m1:Movie)<-[:ACTS_IN]-(bacon0:Actor {name: "Kevin Bacon"}) RETURN bacon2.name')
for record in result:
    outputStr += record['bacon2.name'] + '\n'
outputStr += '\n'

# List which genres have movies where Tom Hanks starred in.
# OUTPUT: genre
outputStr += '### Q6 ###\n'
result = transaction.run('MATCH (tom:Actor {name: "Tom Hanks"})-[:ACTS_IN]->(tomHanksMovies) RETURN DISTINCT tomHanksMovies.genre AS genre')
for record in result:
    outputStr += record['genre'] + '\n'
outputStr += '\n'

# Show which directors have directed movies in at least 2 different genres.
# OUTPUT: director name, number of genres
outputStr += '### Q7 ###\n'
result = transaction.run('MATCH (director:Director)-[:DIRECTED]->(m:Movie) WITH director, COUNT(m.genre) as num_of_genres WHERE num_of_genres >= 2 RETURN director.name, num_of_genres')
for record in result:
    outputStr += record['director.name'] + ', ' + str(record['num_of_genres']) + '\n'
outputStr += '\n'

# Show the top 5 pairs of actor, director combinations, in descending order of frequency of occurrence.
# OUTPUT: director's name, actors' name, number of times director directed said actor in a movie
outputStr += '### Q8 ###\n'
result = transaction.run('MATCH (actor:Actor)-[:ACTS_IN]->(m:Movie)<-[:DIRECTED]-(director:Director) RETURN director.name, actor.name, COUNT(m) as num_Movie ORDER BY num_Movie DESC LIMIT 5')
for record in result:
    outputStr += record['director.name'] + ', ' + record['actor.name'] + ', ' + str(record['num_Movie']) + '\n'

with open("output.txt", "w", encoding='utf-8') as outputFile:
    outputFile.write(outputStr)

transaction.close()
session.close()