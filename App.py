import streamlit as st
import json
import time
from LoginApp import Page
import datetime
import warnings
import os
import datetime
import pytz
from CryptTech import Recipes
import AdminPanel as ap

hide_st_style = """
		<style>
		header {visibility: hidden;}
		footer {visibility: hidden;}
  		</style>
  		"""

st.markdown(hide_st_style, unsafe_allow_html = True)

warnings.filterwarnings("ignore")

Page.main()

if "user" in st.session_state:
	UserDetails = st.session_state["user"]
	#st.write(UserDetails)
	st.session_state["LoginVal"] = True
else:
	st.session_state["LoginVal"] = False

def main():
	if st.session_state["LoginVal"]:
		st.session_state['page'] = "MainRoom"
		UserName = UserDetails["Name"]
		Role = UserDetails["Role"]
		Status = UserDetails["AccVerifStatus"]
		if UserName == "Admin":
			ap.Scrapper()
		else:
			Role = "Lead"
			if Role == "Lead" and Status == "Verified":
				LeadPanel()
			elif Role == "Member" and Status == "Verified":
				MemberPanel()
			else:
				st.write("You are not Authorized Yet!!")
def LeadPanel():
	Projects = UserDetails["Projects"]
	for project in Projects:
		with st.expander(project):
			ProjectMeetFile = "MeetingNotes/" + project
			ProjectDetailsFile = "Projects/" + project + ".pjs"
			
			PjDetails = FileReader(ProjectDetailsFile)
			TeamMembers = PjDetails["Team"]
			Tasks = PjDetails["Tasks"]
			SelMem = st.selectbox(Team, TeamMembers)
			
			df = pd.DataFrame(columns = ["Task", "Status", "Deadline"])
			for i in Tasks[SelMem]:
				newRow = pd.DataFrame({"Task": i["Task"], "Status": i["Status"], "Deadline": i["Deadline"]})
				df = pd.concat([df, newRow], ignore_index = True)
			st.dataframe(df)
	if st.checkbox("Create New Project"):
		CreateProject()

def CreateProject():
	dir = os.listdir("UserAcc")
	Team = []
	Team.append(UserDetails["Name"] + ".ua")
	ProjName = st.text_input("Enter the Project Name")
	ProjDescp = st.text_input("Description")

	dirs = os.listdir("UserAcc")
	for i in dirs:
		if i in Team:
			dirs.remove(i)
			dirs.remove("Admin.ua")
	Mem = st.selectbox("Select Team", dirs, placeholder = "Select ur Team Members")
	st.write("Team Members")
	Team.append(Mem)
	if len(Team) != 0:
		for i in Team:
			st.write(i)
	if st.button("Create"):
		if ProjName.strip() != "":
			for i in Team:
				Path = "UserAcc/" + i + ".ua"
				UsAcc = FileReader(Path)
				UsAcc["Projects"].append(ProjName.strip())
				FileWriter(Path, UsAcc)
			PjDetails = {"Description": ProjDescp, "MeetSessions": [], "Team": Team, "Tasks": []}
			Path = "Projects/" + ProjName.strip() + ".pjs"
			FileWriter(Path, PjDetails)
			Team = []
			return 0
		else:
			st.error("Enter a Valid Project Name")

def CreateMeetSession(ProjName):
	Path = "Projects/" + ProjName + ".pjs"
	PjDetails = FileReader(Path)
			
				
def FileReader(Path):
	with open(Path, "r") as File:
		PjDetails = json.load(File)
	return PjDetails

def FileWriter(Path, Details):
	with open(Path, "w") as File:
		json.dump(Details, File)
		

if __name__ == "__main__":
	main()
