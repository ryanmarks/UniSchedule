from CourseSegment import CourseSegment
from TimeBlock import TimeBlock
from pprint import pprint

class Course():
	def __init__(self,dept,course_code,course_name,course_term,course_section):

		self.department=dept
		self.name=course_name
		self.code=course_code.upper()
		self.term=course_term #Using McMaster's system with Semester 1 or 2 with semester 3 being both semesters
		self.section=course_section.upper() #Courses are either DAY or EVE
		self.segments=dict()

		#Coincident segments are held in a 2D Dictionary.
		#The first key is a character that represents the segment type
		#The second is a scheduling key generated by the segment.
		#Two segments with the same schedule will have the same scheduling key
		self.coincident_segments=dict(dict())

	def get_segments(self):#Get the tuple key of every segment
		keys=[self.segments[s].tuple_key() for s in self.coincident_segments]
		return keys

	def add(self,segment):#Add a given segment to the dictionary of segments
		self.segments[segment.name]=segment

	def set_segments(self,given_segment_names):
		#Set the coincident_segments to the segments named in given_segment_names
		segments = [self.segments[name] for name in given_segment_names]
		self.consolidate_segments(segments)


	def consolidate_segments(self, given_segments = None):
		if given_segments is None:
			given_segments = self.segments.values()
		for segment in given_segments:
			segment_type=segment.name[0]# Will be either 'C','L', or 'T'

			#The scheduling key will not be unique for classes happening at the
			#same time, storing classes that are functionally identical in the
			#same list makes things a good deal more efficient
			scheduling_key=segment.tuple_key()

			try:
				self.coincident_segments[segment_type][scheduling_key].append(segment)
			except KeyError:
				#Will be raised if either coincident_segments[segment_type] does not exist
				#or if coincident_segments[segment_type][scheduling_key] doesn't
				try:
					#Try to create [segment_type][scheduling_key] as a new list
					self.coincident_segments[segment_type][scheduling_key]=[segment,]
				except KeyError:
					#This means coincident_segments[segment_type] doesn't exist
					#and that we must create it before adding the segment
					self.coincident_segments[segment_type]=dict()
					self.coincident_segments[segment_type][scheduling_key]=[segment]

	def key_to_names(self,tuple_key):
		names=[]
		for element in  self.coincident_segments[type][tuple_key]:
			names.append(element.name)
		return names

	def to_string(self):
		out=self.department+"\n"
		out+=self.code+"\n"
		out+=self.name+"\n"
		out+=str(self.term)+"\n"
		out+=self.section+"\n"
		for segment in self.segments.keys():
			out+=segment+"\n"+self.segments[segment].to_string()+"\n"
		return out

	def tuple_key(self):
		return (self.department,self.code,self.term,self.section)
"""
chem_101=Course("Chemistry","1C01","Intro To Chemistry",1,"DAY")

chem_core_1=CourseSegment()
chem_core_1.prof="Chem Prof"
chem_core_1.name="C01"
chem_core_1.add(TimeBlock(1,8,00,9,00,1))
chem_core_1.add(TimeBlock(2,8,30,9,30,1))

chem_core_2=CourseSegment()
chem_core_2.prof="Chem Prof"
chem_core_2.name="C02"
chem_core_2.add(TimeBlock(1,8,00,9,00,1))
chem_core_2.add(TimeBlock(2,8,30,9,30,1))

chem_lab_1=CourseSegment()
chem_lab_1.name="L01"
chem_lab_1.add(TimeBlock(4,9,00,10,30,1))
chem_lab_1.add(TimeBlock(1,9,00,10,0,1))

chem_lab_2=CourseSegment()
chem_lab_2.name="L02"
chem_lab_2.add(TimeBlock(4,9,00,10,30,1))
chem_lab_2.add(TimeBlock(1,9,00,10,0,1))

chem_101.add(chem_core_1)
chem_101.add(chem_core_2)
chem_101.add(chem_lab_1)
chem_101.add(chem_lab_2)

chem_101.consolidate_segments()
for type in chem_101.coincident_segments.keys():
	print(type)
	for i in chem_101.coincident_segments[type].keys():
		print(chem_101.key_to_names(i))

"""
