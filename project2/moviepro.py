import sqlite3 as lite
import csv
import re
import pandas
import string
con = lite.connect('cs1656.sqlite')

with con:
	cur = con.cursor() 

	########################################################################		
	### CREATE TABLES ######################################################
	########################################################################		
	# DO NOT MODIFY - START 
	cur.execute('DROP TABLE IF EXISTS Actors')
	cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

	cur.execute('DROP TABLE IF EXISTS Movies')
	cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

	cur.execute('DROP TABLE IF EXISTS Directors')
	cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

	cur.execute('DROP TABLE IF EXISTS Cast')
	cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

	cur.execute('DROP TABLE IF EXISTS Movie_Director')
	cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
	# DO NOT MODIFY - END

	########################################################################		
	### READ DATA FROM FILES ###############################################
	########################################################################		
	# actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
	# UPDATE THIS
	actors = []
	with open('actors.csv') as actorFile:
		fileReader = csv.reader(actorFile)
		for row in fileReader:
			actors.append(row)
	
	cast = []
	with open('cast.csv') as castFile:
		fileReader = csv.reader(castFile)
		for row in fileReader:
			cast.append(row)
	
	directors = []
	with open('directors.csv') as dirFile:
		fileReader = csv.reader(dirFile)
		for row in fileReader:
			directors.append(row)

	movieDir = []
	with open('movie_dir.csv') as movieDirFile:
		fileReader = csv.reader(movieDirFile)
		for row in fileReader:
			movieDir.append(row)

	movies = []
	with open('movies.csv') as moviesFile:
		fileReader = csv.reader(moviesFile)
		for row in fileReader:
			movies.append(row)
	########################################################################		
	### INSERT DATA INTO DATABASE ##########################################
	########################################################################		
	# UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
	for actor in actors:
		actor[0] = actor[0].replace("'", "''")
		actor[1] = actor[1].replace("'", "''")
		actor[2] = actor[2].replace("'", "''")
		actor[3] = actor[3].replace("'", "''")
		cur.execute("INSERT INTO Actors VALUES (" + actor[0] + ", '" + actor[1] + "', '" + actor[2] + "', '" + actor[3] + "')")
	for person in cast:
		person[0] = person[0].replace("'", "''")
		person[1] = person[1].replace("'", "''")
		person[2] = person[2].replace("'", "''")
		cur.execute("INSERT INTO Cast VALUES (" + person[0] + ", " + person[1] + ", '" + person[2] + "')")
	for director in directors:
		director[0] = director[0].replace("'", "''")
		director[1] = director[1].replace("'", "''")
		director[2] = director[2].replace("'", "''")
		cur.execute("INSERT INTO Directors VALUES (" + director[0] + ", '" + director[1] + "', '" + director[2] + "')")
	for movDir in movieDir:
		movDir[0] = movDir[0].replace("'", "''")
		movDir[1] = movDir[1].replace("'", "''")
		cur.execute("INSERT INTO Movie_Director VALUES (" + movDir[0] + ", " + movDir[1] + ")")
	for movie in movies:
		movie[0] = movie[0].replace("'", "''")
		movie[1] = movie[1].replace("'", "''")
		movie[2] = movie[2].replace("'", "''")
		movie[3] = movie[3].replace("'", "''")
		cur.execute("INSERT INTO Movies VALUES (" + movie[0] + ", '" + movie[1] + "', " + movie[2] + ", " + movie[3] + ")")
	#cur.execute("INSERT INTO Actors VALUES(1001, 'Harrison', 'Ford', 'Male')") 
	#cur.execute("INSERT INTO Actors VALUES(1002, 'Daisy', 'Ridley', 'Female')")   

	#cur.execute("INSERT INTO Movies VALUES(101, 'Star Wars VII: The Force Awakens', 2015, 8.2)") 
	#cur.execute("INSERT INTO Movies VALUES(102, 'Rogue One: A Star Wars Story', 2016, 8.0)")

	#cur.execute("INSERT INTO Cast VALUES(1001, 101, 'Han Solo')")  
	#cur.execute("INSERT INTO Cast VALUES(1002, 101, 'Rey')")  

	#cur.execute("INSERT INTO Directors VALUES(5000, 'J.J.', 'Abrams')")  
	con.commit()


	########################################################################		
	### QUERY SECTION ######################################################
	########################################################################		
	queries = {}

	# DO NOT MODIFY - START 	
	# DEBUG: all_movies ########################
	queries['all_movies'] = '''
SELECT * FROM Movies
'''	
	# DEBUG: all_actors ########################
	queries['all_actors'] = '''
SELECT * FROM Actors
'''	
	# DEBUG: all_cast ########################
	queries['all_cast'] = '''
SELECT * FROM Cast
'''	
	# DEBUG: all_directors ########################
	queries['all_directors'] = '''
SELECT * FROM Directors
'''	
	# DEBUG: all_movie_dir ########################
	queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''	
	# DO NOT MODIFY - END

	########################################################################		
	### INSERT YOUR QUERIES HERE ###########################################
	########################################################################		
	# NOTE: You are allowed to also include other queries here (e.g., 
	# for creating views), that will be executed in alphabetical order.
	# We will grade your program based on the output files q01.csv, 
	# q02.csv, ..., q12.csv

	# Q01 ########################		
	queries['q01'] = '''
	SELECT DISTINCT a.fname, a.lname
	FROM Cast c, Actors a
	WHERE c.aid =  a.aid 
	AND c.aid IN (SELECT c.aid 
				  FROM Cast c, Movies m
				  WHERE m.mid = c.mid AND m.year < 1991 AND m.year > 1979)
	AND c.aid IN (SELECT c.aid
				  FROM Cast c, Movies m
				  WHERE m.mid = c.mid AND m.year > 1999)
	ORDER BY a.lname, a.fname
'''
	# Q02 ########################		
	queries['q02'] = '''
	SELECT title, year
	FROM Movies
	WHERE year IN (SELECT year
				   FROM Movies
				   WHERE title = 'Rogue One: A Star Wars Story')
	   AND rank > (SELECT rank
	   			   FROM Movies
				   WHERE title = 'Rogue One: A Star Wars Story')
	ORDER BY Movies.title
'''	

	# Q03 ########################		
	queries['q03'] = '''
	SELECT a.fname, a.lname, COUNT(m.title) as numMov
	FROM Actors a, Cast c, Movies m
	WHERE a.aid = c.aid AND c.mid = m.mid AND title like '%Star Wars%'
	GROUP BY a.lname, a.fname
	ORDER BY numMov DESC
'''	

	# Q04 ########################		
	queries['q04'] = '''
	SELECT a.fname, a.lname
	FROM Actors a
	WHERE NOT a.aid IN (SELECT a2.aid
						FROM Actors a2, Cast c2, Movies m2
						WHERE a2.aid = c2.aid AND m2.mid = c2.mid AND m2.year > 1984)
	ORDER BY a.lname, fname
'''	

	# Q05 ########################		
	queries['q05'] = '''
	SELECT d.fname, d.lname, COUNT(DISTINCT md.mid) AS num_films
	FROM Directors d, Movie_Director md
	WHERE d.did = md.did
	GROUP BY d.did
	ORDER BY num_films DESC
	LIMIT 20
'''	

	# Q06 ########################
	queries['q06'] = '''
	SELECT m.title, COUNT(DISTINCT c.aid) AS num_cast
	FROM Movies m, Cast c
	WHERE c.mid = m.mid
	GROUP BY m.mid
	HAVING  num_cast >= (SELECT MIN(num_cast2)
						 FROM (SELECT COUNT(c2.aid) AS num_cast2
						 	   FROM Movies m2, Cast c2
							   WHERE c2.mid = m2.mid
							   GROUP BY m2.mid
							   ORDER BY num_cast2 DESC
							   LIMIT 10))
	ORDER BY num_cast DESC
'''	

	# Q07 ########################
	cur.execute('DROP VIEW IF EXISTS Movgender')
	createView = '''
	CREATE VIEW Movgender AS 
		SELECT m1.title AS title, a.gender AS gender 
		FROM Actors a, Cast c1, Movies m1
		WHERE c1.aid = a.aid AND c1.mid = m1.mid
		GROUP BY fname, lname, m1.title
'''
	cur.execute(createView)
	cur.execute('DROP VIEW IF EXISTS MovCount')
	createView2 = '''
	CREATE VIEW MovCount AS 
		SELECT Movgender.title AS title, SUM(CASE WHEN Movgender.gender = "Female" THEN 1 ELSE 0 END) AS F, SUM(CASE WHEN Movgender.gender = "Male" THEN 1 ELSE 0 END) AS M 
		FROM Movgender 
		GROUP BY Movgender.title
'''
	cur.execute(createView2)
	
	queries['q07'] = '''
	SELECT MovCount.title, MovCount.F, MovCount.M
	FROM MovCount
	WHERE MovCount.F > MovCount.M
	ORDER BY MovCount.title
'''	

	# Q08 ########################		
	queries['q08'] = '''
	SELECT fname, lname, COUNT(DISTINCT did) AS numDir
	FROM Actors NATURAL JOIN Cast NATURAL JOIN Movies NATURAL JOIN Movie_Director
	GROUP BY fname
	HAVING numDir >= 7
	ORDER BY numDir DESC
'''	

	# Q09 ########################		
	queries['q09'] = '''
	SELECT a.fname, a.lname, COUNT(DISTINCT m.title) as numMovies
	FROM Actors a , Movies m
	WHERE a.fname like 'T%' AND m.year = (SELECT MIN(m2.year)
									  	  FROM Actors a2, Cast c2, Movies m2
										  WHERE a2.aid = c2.aid AND c2.mid = m2.mid)
	GROUP BY a.fname, a.lname
	ORDER BY numMovies DESC
'''	

	# Q10 ########################		
	queries['q10'] = '''
	SELECT a.lname, m.title
	FROM Actors a 
	INNER JOIN Cast c ON a.aid = c.aid 
	INNER JOIN Movies m ON c.mid = m.mid 
	INNER JOIN Movie_Director md ON c.mid = md.mid 
	INNER JOIN Directors d ON d.did = md.did
	WHERE a.lname = d.lname
	ORDER BY a.lname
'''	
	# creating view to get all actors, cast, movies, movie_director, director that had Kevin Bacon in it
	# Q11 ########################
	cur.execute('DROP VIEW IF EXISTS KevBacon')
	createView = '''
	CREATE VIEW KevBacon AS
		SELECT m1.title AS title, m1.mid AS mid
		FROM Actors a 
		INNER JOIN Cast c1 ON c1.aid = a.aid
		INNER JOIN Movies m1 ON m1.mid = c1.mid
		INNER JOIN Movie_Director md1 ON m1.mid = md1.mid
		INNER JOIN Directors d1 ON d1.did = md1.did
		WHERE a.fname = "Kevin" AND a.lname = "Bacon"
'''
	cur.execute(createView)
	# getting all actors whose Bacon number is 2 (acted in same filme as actors w/ Bacon number 1)
	queries['q11'] = '''
	SELECT a2.fname, a2.lname
	FROM KevBacon kb
	INNER JOIN Cast c1 ON c1.mid = kb.mid
	INNER JOIN Actors a1 ON a1.aid = c1.aid
	INNER JOIN Cast c2 ON c2.aid = a1.aid
	INNER JOIN Movies m1 ON m1.mid = c2.mid
	INNER JOIN Cast c3 ON c3.mid = m1.mid
	INNER JOIN Actors a2 ON a2.aid = c3.aid
	WHERE c3.mid != kb.mid AND a1.aid != c3.aid AND a1.fname != "Kevin" AND a1.lname != "Bacon"
	GROUP BY a2.fname, a2.lname
'''	

	# Q12 ########################		
	queries['q12'] = '''
	SELECT a.fname, a.lname, COUNT(m.mid), AVG(m.rank) AS score
	FROM Actors a
	INNER JOIN Cast c ON a.aid = c.aid
	INNER JOIN Movies m ON c.mid = m.mid
	GROUP BY a.aid
	ORDER BY score DESC
	LIMIT 20
'''	


	########################################################################		
	### SAVE RESULTS TO FILES ##############################################
	########################################################################		
	# DO NOT MODIFY - START 	
	for (qkey, qstring) in sorted(queries.items()):
		try:
			cur.execute(qstring)
			all_rows = cur.fetchall()
			
			print ("=========== ",qkey," QUERY ======================")
			print (qstring)
			print ("----------- ",qkey," RESULTS --------------------")
			for row in all_rows:
				print (row)
			print (" ")

			save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
			if (save_to_file):
				with open(qkey+'.csv', 'w') as f:
					writer = csv.writer(f)
					writer.writerows(all_rows)
					f.close()
				print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
		
		except lite.Error as e:
			print ("An error occurred:", e.args[0])
	# DO NOT MODIFY - END
	
