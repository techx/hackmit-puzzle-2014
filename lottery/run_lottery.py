import random
import re

class Person():
	def __init__(self,p_id,p_account_id,p_team_id,p_name,p_gender,p_school_id,p_school,p_adult,p_location,p_invite_code,p_interests,p_email):
		self.uid = p_id
		self.account_id = p_account_id
		self.team_id = p_team_id
		self.name = p_name
		self.gender = p_gender
		self.school_id = p_school_id
		self.school = p_school
		self.adult = p_adult
		self.location = p_location
		self.invite_code = p_invite_code
		self.interests = p_interests
		self.email = p_email

class Team():
	def __init__(self,person):
		self.admitted = 0
		self.people = [person]

def extract_individuals_info():
	all_users = open("users.txt","r")
	user_arr = all_users.read().split("),(")
	email_dict = dict()
	for user in user_arr:
		temp_user = user.split(",")
		email_dict[temp_user[0]] = temp_user[1][1:-1]

	all_people = open("sql_dump.txt","r")
	people_arr = all_people.read().split("),(")
	regex = "[0-9]+,[0-9]+,[0-9A-Za-z]+,'.*','[A-Za-z]+',[0-9A-Za-z]+,'.+',[0-9],.*,'.*','.*'"

	team_dict = dict()

	individual_team_counter = 1
	for person in people_arr:
		if re.search(regex,person):
			temp_person = person.split(',')
			p_id = temp_person[0]
			p_account_id = temp_person[1]
			p_team_id = temp_person[2]
			p_name = temp_person[3][1:-1]
			p_gender = temp_person[4][1:-1]
			p_school_id = temp_person[5]
			p_school = temp_person[6][1:-1]
			p_adult = temp_person[7]
			p_location = temp_person[8][1:-1]
			p_invite_code = temp_person[9][1:-1]
			p_interests = ",".join(temp_person[10:])[1:-1]
			p_email = email_dict[p_account_id]

			if p_team_id == 'NULL':
				p_team_id = str(individual_team_counter) + 'a'
				individual_team_counter += 1

			p = Person(p_id, p_account_id, p_team_id, p_name, p_gender, p_school_id, p_school, p_adult, p_location, p_invite_code, p_interests,p_email)
			if p_team_id in team_dict.keys():
				team_dict[p_team_id].people.append(p)
			else:
				team_dict[p_team_id] = Team(p)

			if len(team_dict[p_team_id].people) > 4:
				print 'ERROR: team too large'

	return team_dict

def count_admits(teams):
	count = 0
	for team in teams.keys():
		if teams[team].admitted == 1:
			count += len(teams[team].people)
	return count

def main(total_number_of_admits,female_admit_percentage):
	# Teams: teams will be entered together (one entry) in the lottery, with the average of their member chances as the total chance for the team. 
	teams = extract_individuals_info()

	file_codes = open("valid_codes.txt","r")
	valid_codes = []
	for line in file_codes:
		valid_codes.append(line.strip())

	file_admit = open("auto_admits.txt","r")
	auto_admits = []
	for line in file_admit:
	  	if line[0:1] != "#":
			auto_admits.append(line.strip())

	count = 0

	for team in teams.keys():
		for member in teams[team].people:
			# Case 1: Solved the Puzzle
			# Every member (up to 4) on a team with a puzzle code will be admitted (max 200; estimated 100)
			if member.invite_code in valid_codes:
			 	teams[team].admitted = 1

			# Case 2: MIT Student
			# Every MIT student who registered will be admitted (estimated 400)
			if member.school == "Massachusetts Institute of Technology (Massachusetts)":
				teams[team].admitted = 1
				count += 1
				if not "@mit.edu" in member.email.lower():
					print member.name+ " <" + member.email + "> "

			# Case 3: Corruption with a Twist
			# Individuals who have been exceptionally helpful with outreach efforts will be admitted. 
			# Hackathon organizer leads will be admitted.
			# Participants known for a winning record will be admitted. 
			# A limited number of people can be added to this list with good reason.
			# This list cannot contain more than 50 people.

			# elif member.name in auto_admits:
			# 	teams[team].admitted = 1
			# 	print member.name



	# Case 4: Lottery Algorithm
	# [we want to admit 30% women] 
	not_admitted_female = 0
	not_admitted_non_female = 0
	num_slots_remaining_female = total_number_of_admits*female_admit_percentage
	num_slots_remaining_non_female = total_number_of_admits*(1-female_admit_percentage)
	for team in teams.keys():
		if teams[team].admitted != 1:
			for member in teams[team].people:
				if member.gender == 'female':
					not_admitted_female += 1
				else:
					not_admitted_non_female += 1
		else:
			for member in teams[team].people:
				if member.gender == 'female':
					num_slots_remaining_female -= 1
				else:
					num_slots_remaining_non_female -= 1

	# print "percentage female: " + str(female*1.0/(female + non_female))
	female_admit_chance = num_slots_remaining_female/not_admitted_female
	non_female_admit_chance = num_slots_remaining_non_female/not_admitted_non_female
	# print "lottery female admit chance: " + str(female_admit_chance)
	# print "lottery non female admit chance: " + str(non_female_admit_chance)

	for team in teams.keys():
		if teams[team].admitted != 1:
			cumulative_percentage_chance = 0
			for member in teams[team].people:
				if member.gender == 'female':
					cumulative_percentage_chance += female_admit_chance
				else:
					cumulative_percentage_chance += non_female_admit_chance
			percentage_admission_chance = cumulative_percentage_chance/len(teams[team].people)
			# print str(percentage_admission_chance)
			if random.random() < percentage_admission_chance:
				teams[team].admitted = 1

	# Case 5: Bus Adjustments
	# [we want all buses to be full]
	# Adjust admits for bus numbers
	#  -- Case 1: more than can fit on a bus were admitted. Fix by randomly choosing people to cut.
	#  -- Case 2: less than can fit on a bus were admitted. Fix by randomly lotterying from that school.
	# bus_schools = ["Dartmouth College (New Hampshire)","University of Pennsylvania (Pennsylvania)","Rutgers University-New Brunswick (New Jersey)","Columbia University in the City of New York (New York)","New York University (New York)","Princeton University (New Jersey)","Yale University (Connecticut)","Brown University (Rhode Island)","University of Maryland-College Park (Maryland)","Cornell University (New York)","Carnegie Mellon University (Pennsylvania)"]
	# bus_dict = dict()

	# for team in teams.keys():
	# 	if teams[team].admitted == 1:
	# 		for member in teams[team].people:
	# 			if member.school in bus_schools or "mcgill" in member.school.lower() or "waterloo" in member.school.lower():
	# 				if member.school in bus_dict.keys():
	# 					bus_dict[member.school] += 1
	# 				else:
	# 					bus_dict[member.school] = 1


	# for bus in bus_dict.keys():
	# 	if bus_dict[bus] > 5:
	# 		print str(bus) + ": " + str(bus_dict[bus])

	admits = open("admitted_students.txt","w")
	waitlisted = open("waitlisted_students.txt","w")

	for team in teams.keys():
		for member in teams[team].people:
			if teams[team].admitted == 1:
				admits.write(member.name + " <" + member.email + ">\n")
			else:
				waitlisted.write(member.name + " <" + member.email + ">\n")

	admits.close()
	waitlisted.close()


	print "number of admits: " + str(count_admits(teams))


main(total_number_of_admits=1400, female_admit_percentage=0.3)













