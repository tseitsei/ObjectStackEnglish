#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Juha Kari 2015.

import sys
import time
import datetime
import sqlite3

class ObjectStack:
	"""A simple object stack class"""
	
	def __init__(self):
		self.stack = []
	
	def add_object(self, object):
		self.stack.append(object)
	
	def top(self):
		return self.stack[len(self.stack)-1:][0]
	
	def len(self):
		return len(self.stack)
	
	def __len__(self):
		return len(self.stack)
		
	def get_possible_next_objects(self, change_condition, available_objects):
		# All different shapes.
		shapes = "sScCtT"
		# All different colors.
		colors = "123"
		
		possible_shapes = ""
		possible_colors = ""
		
		# First object (change_condition == "*").
		if change_condition == "*":
			print("First tile. All choices are possible.")
			possible_shapes = shapes
			possible_colors = colors
		else:
			# Form changes.	
			if change_condition == "f":
				if self.top()[0] == "s":
					possible_shapes = "ct"
				elif self.top()[0] == "S":
					possible_shapes = "CT"
				elif self.top()[0] == "c":
					possible_shapes = "st"
				elif self.top()[0] == "C":
					possible_shapes = "ST"
				elif self.top()[0] == "t":
					possible_shapes = "sc"
				elif self.top()[0] == "T":
					possible_shapes = "SC"
				
				possible_colors = self.top()[2]
			
			# Size changes.	
			if change_condition == "s":
				if self.top()[0] == "s":
					possible_shapes = "S"
				elif self.top()[0] == "S":
					possible_shapes = "s"
				elif self.top()[0] == "c":
					possible_shapes = "C"
				elif self.top()[0] == "C":
					possible_shapes = "c"
				elif self.top()[0] == "t":
					possible_shapes = "T"
				elif self.top()[0] == "T":
					possible_shapes = "t"
				
				possible_colors = self.top()[2]
			
			# Color changes.	
			if change_condition == "c":
				possible_colors = [x for x in colors if x != self.top()[2]]
				possible_shapes = self.top()[0]
		
		combinations = [x + " " + y for x in possible_shapes for y in possible_colors]
		return [x for x in combinations if x in available_objects]
	
	def is_possible_next_object(self, change_condition, available_objects, candidate):
		# All different shapes.
		shapes = "sScCtT"
		# All different colors.
		colors = "123"
		
		if candidate in self.get_possible_next_objects(change_condition, available_objects):
			return True
		else:
			return False
		
	def __str__(self):
		return str(self.stack)

	def __unicode__(self):
		return unicode(self.stack)

class ObjectDecoder:
	"""A simple object stack decoder"""
	
	def is_valid(self, object):
		valid = True
		if len(object) < 3:
			valid = False
		else:
			if object[0].isalpha() == False:
				valid = False
			if object[2].isdigit() == False:
				valid = False
		return valid
	
	def decode(self, object):
		size = ""
		color = ""
		shape = ""
		
		if self.is_valid(object) == False:
			return "Unknown tile"
		else:
			if object[0].islower():
				size = "A small"
			elif object[0].isupper():
				size = "A large"
			
			if object[0].lower() == 's':
				shape = "square"
			elif object[0].lower() == 'c':
				shape = "circle"
			elif object[0].lower() == 't':
				shape = "triangle"
			
			if object[2] == '1':
				color = "red"
			elif object[2] == '2':
				color = "green"
			elif object[2] == '3':
				color = "blue"
		
		return size + " " + color + " " + shape

class ObjectStackGame:
	"""A simple object stack game"""
	
	def play(self):
		# Creating a sqlite3 connection.
		conn = sqlite3.connect('ObjectStack.db')
		# Creating a cursor.
		c = conn.cursor()
		
		# Querying the maximum score from the database.
		query = "SELECT MAX(score),player_name FROM statistics;"
		c.execute(query)
		result = c.fetchone()
		(highscore, hs_player_name) = (int(result[0]), result[1])
		
		# Begin time of this game.
		begin_time = time.time()
		
		# End time of this game.
		end_time = time.time()
		
		# All available objects in the list.
		o = []
		
		# Stack.
		s = ObjectStack()
		
		# Decoder.
		d = ObjectDecoder()
		
		# Creating initial tiles and putting them into the list.
		o.append("s 1")
		o.append("S 1")
		o.append("s 2")
		o.append("S 2")
		o.append("s 3")
		o.append("S 3")
		o.append("c 1")
		o.append("C 1")
		o.append("c 2")
		o.append("C 2")
		o.append("c 3")
		o.append("C 3")
		o.append("t 1")
		o.append("T 1")
		o.append("t 2")
		o.append("T 2")
		o.append("t 3")
		o.append("T 3")
		
		number_of_objects = len(o)
	
		condition = "*"
		win = False
		
		print("****************")
		print("* OBJECT STACK *")
		print("****************")
		print("Highscore: %s/%i." % (hs_player_name, highscore))
		
		# Repeat until there are no more available tiles.
		while len(o) > 0 and len(s.get_possible_next_objects(condition, o)) > 0 and win == False:
			print("Available tiles:")
			print(o)
			
			next_object = input("Choose the tile to be added on the stack: ")
			if d.is_valid(next_object):
				print("You chose the tile: " + next_object + ". " + d.decode(next_object) + ".")
			else:
				print("Your input is not a valid tile!")
			
			if s.is_possible_next_object(condition, o, next_object):
				s.add_object(next_object)
				print("Current stack: " + str(s))
				o.remove(next_object)
				
				print("Topmost tile: " + s.top() + ". " + d.decode(s.top()) + ".")
				
				print("Available tiles:")
				print(o)
				
				# If there are no more available tiles left, the game is won.
				if len(o) <= 0:
					win = True
				else:
					condition = ""
					while condition not in ["f", "s", "c"]:
						condition = input("Choose the change condition for the next tile (f/s/c): ")
					if condition in ["f", "s", "c"]:
						print("You chose the condition: " + condition)
						print("Possibilities for the next tile to be stacked:")
						
						possible_shapes = s.get_possible_next_objects(condition, o)
						print(possible_shapes)
						
						#if len(possible_shapes) <= 0 and len(s) >= number_of_objects:
						#	win = True
					else:
						print("Your input is not a valid condition!")
			else:
				print("The tile you chose is not available.")
		
		# End time of this game.
		end_time = time.time()
		# Duration of this game in seconds.
		duration = end_time - begin_time
		duration_rounded = round(duration, 2)
		objects_in_stack = len(s)
		unused_objects = len(o)
		
		# Score.
		score = int(round(((1.0 / duration_rounded) * pow(objects_in_stack, 4) * 200), 0))
		if (duration_rounded < 4.0):
			score = 0
		
		if win == True:
			print("Congratulations! You stacked all the tiles!")
		else:
			print("You lost. You could not stack all the tiles.")
		print("You stacked %s tiles and left unstacked %s tiles." % (len(s), len(o)))
		print("The duration of the game was %s seconds." % duration_rounded)
		print("You got %s points." % score)
		if (score > highscore):
			print("You got a new highscore! Previous highscore: %s/%i." % (hs_player_name, highscore))
		if (duration_rounded < 4.0):
			print("No points are given for a game under 4 seconds.")
		
		# Asking the name of the player and saving it into the database with the score.
		player_name = input("Please input your name: ")
		
		# Saving the statistics into the database.
		query = "INSERT INTO statistics (begin_time, end_time, duration_rounded, objects_in_stack, unused_objects, score, win, stack, unused, player_name) VALUES ('%s', '%s', '%s', %i, %i, %i, '%s', \"%s\", \"%s\", \"%s\");"
		value = (begin_time, end_time, duration_rounded, objects_in_stack, unused_objects, score, win, str(s), str(o), player_name)
		c.execute(query % value)
		
		# Saving the changes.
		conn.commit()
		
		# Closing the connection to the database.
		conn.close()

if __name__ == "__main__":
	# Checking that the user has at least Python 3.
	print("The Python version is " + sys.version)
	
	if sys.version_info[0] < 3:
		print("This program requires Python 3.0 -interpreter. Shutting down.")
		sys.exit(1)
	
	# Retrieving sqlite3 library version.
	sqlite3lib_version = sqlite3.version
	# Retrieving sqlite3 program version.
	sqlite3_version = sqlite3.sqlite_version
	
	print("SQLite library: %s. SQLite: %s." % (sqlite3lib_version, sqlite3_version))
	
	# Creating the game object.
	g = ObjectStackGame()
	
	# Playing the game.
	try:
		g.play()
	except (KeyboardInterrupt, SystemExit, EOFError):
		print("Shutting down because of an interrupt.")
	except sqlite3.OperationalError:
		print("Database error. Shutting down.")
	except:
		pass
