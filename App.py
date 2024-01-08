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
import pandas as pd

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
			if Role == "Lead" and Status == "Verified":
				tab1, tab2, tab3 = st.tabs(["Projects", "New Project", "Meetings"])
				with tab1:
					LeadPanel()
				with tab2:
					CreateProject()
				with tab3:
					MeetingPanel()
					
			elif Role == "Member" and Status == "Verified":
				tab1, tab2 = st.tabs(["Projects", "Meetings"])
				with tab1:
					MemberPanel()
				with tab2:
					MeetingPanel()
			else:
				path = "LoginApp/UnVerified.uv"
				with open(path, "r") as File:
					k = json.load(File)
				if UserName not in k["Names"]:
					st.error("Your Account Creation was Suspended")
				else:
					st.error("Still in Review, You are not Authorized Yet!!")
def LeadPanel():
	Projects = UserDetails["Projects"]
	project = st.selectbox("Select a Project", Projects, index = None)
	if project != None:
		with st.expander("Expand For more Details"):
			ProjectMeetFile = "MeetingNotes/" + project
			ProjectDetailsFile = "Projects/" + project + ".pjs"
			
			PjDetails = FileReader(ProjectDetailsFile)
			TeamMembers = PjDetails["Team"]
			Tasks = PjDetails["Tasks"]
			SelMem = st.selectbox("Team", TeamMembers)
			
			df = pd.DataFrame(columns = ["Task", "Status", "Deadline"])
			for i in range(0, len(Tasks[SelMem])):
				newRow = pd.DataFrame({"Task": Tasks[SelMem][i]["Task"], "Status": Tasks[SelMem][i]["Status"], "Deadline": Tasks[SelMem][i]["Deadline"]})
				df = pd.concat([df, newRow], ignore_index = True)
			st.dataframe(df)
def MemberPanel():
	Projects = UserDetails["Projects"]
	project = st.selectbox("Select a Project", Projects, index = None)
	if project != None:
		with st.expander("Expand For more Details"):
			ProjectMeetFile = "MeetingNotes/" + project
			ProjectDetailsFile = "Projects/" + project + ".pjs"
			
			PjDetails = FileReader(ProjectDetailsFile)
			TeamMembers = PjDetails["Team"]
			Tasks = PjDetails["Tasks"]
			SelMem = UserDetails["Name"] + ".ua"
			
			df = pd.DataFrame(columns = ["Task", "Status", "Deadline"])
			for i in range(0, len(Tasks[SelMem])):
				newRow = pd.DataFrame({"Task": Tasks[SelMem][i]["Task"], "Status": Tasks[SelMem][i]["Status"], "Deadline": Tasks[SelMem][i]["Deadline"]})
				df = pd.concat([df, newRow], ignore_index = True)
			st.dataframe(df)

def CreateProject():
	ProjName = st.text_input("Enter the Project Name")
	ProjDescp = st.text_input("Description")

	dirs = os.listdir("UserAcc")
	dirs.remove("Admin.ua")
	dirs.remove(UserDetails["Name"] + ".ua")
	dirs.remove("Test.ua")
	Team = st.multiselect("Select Team", dirs, placeholder = "Select ur Team Members")
	Team.append(UserDetails["Name"] + ".ua")
	if st.button("Create"):
		if ProjName.strip() != "":
			tsks = {}
			for i in Team:
				tsks[i] = []
				Path = "UserAcc/" + i
				UsAcc = FileReader(Path)
				UsAcc["Projects"].append(ProjName.strip())
				FileWriter(Path, UsAcc)
			
			PjDetails = {"Description": ProjDescp, "MeetSessions": [], "Team": Team, "Tasks": tsks, "SessionTitles": []}
			Path = "Projects/" + ProjName.strip() + ".pjs"
			FileWriter(Path, PjDetails)
			Team = []
			st.rerun()
		else:
			st.error("Enter a Valid Project Name")

def MeetingPanel():
	Projects = UserDetails["Projects"]
	project = st.selectbox("Select a Project", Projects, index = None, key = "mp")
	if project != None:
		#with st.expander("Expand For more Details"):
		ProjectMeetFile = "MeetingNotes/" + project
		ProjectDetailsFile = "Projects/" + project + ".pjs"
		PjDetails = FileReader(ProjectDetailsFile)
		MeetSess = PjDetails["SessionTitles"]
		SessionTitles = []
		for i in range(0, len(MeetSess)):
			SessionTitles.append(MeetSess[i]["Title"])
		with st.expander("Past Meetings"):
			SelMeet = st.selectbox("Select a Past Meeting", SessionTitles, index = -1)
			if SelMeet:
				ProjectMeetFile += SelMeet
				st.subheader("Meeting Notes")
				with open(ProjectMeetFile, "r") as file:
					lines = file.readlines()
					for line in lines:
						st.write(line.strip())
	
				SelMeetInd = SessionTitles.index(SelMeet)
				SelMem = st.selectbox("Select a Team Member", list(MeetSess[SelMeetInd]["Tasks"].keys()))
				SelMemTasks = MeetSess[SelMeetInd]["Tasks"][SelMem]
				df = pd.DataFrame(columns = ["Task", "Status", "Deadline"])
				for i in range(0, len(SelMemTasks)):
					newRow = pd.DataFrame({"Task": SelMemTasks[i]["Task"], "Status": SelMemTasks[i]["Status"], "Deadline": SelMemTasks[i]["Deadline"]})
					df = pd.concat([df, newRow], ignore_index = True)
				st.dataframe(df)
	if project:
		CreateMeetSession(project)

def CreateMeetSession(ProjName):
	time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
	Path = "Projects/" + ProjName + ".pjs"
	PjDetails = FileReader(Path)
	NewMeetID = len(PjDetails["SessionTitles"])
	Title = st.text_input("Enter a Title for the Note", value = "MEET_HELD_ON_" + str(time))
	if Title:
		PjDetails["SessionTitles"].append({"Title": Title, "TimeStamp": str(time)})
		FileWriter(Path, PjDetails)
	
	Note = st.text_area("Enter Action Items or Meeting Notes")
	col1, col2 = st.columns(2)
	with col:
		if st.button("Assign"):
			Team = PjDetails["Team"]
			SelMem = st.selectbox("Select a Team Member", Team)
			DeadLine = st.date_input("Select the Deadline", value = "today")
			Status = "Un Resolved"
			if st.button("Send"):
				time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
				PjDetails = FileReader(Path)
				PjDetails["MeetSessions"][NewMeetID]["Tasks"][SelMem].append({"Task": Note, "Status": Status, "Deadline": DeadLine})
				PjDetails["Tasks"][SelMem].append({"Task": Note, "Status": Status, "Deadline": DeadLine})
				FileWriter(Path, PjDetails)
				#---------->Mail
	
			
				
def FileReader(Path):
	with open(Path, "r") as File:
		PjDetails = json.load(File)
	return PjDetails

def FileWriter(Path, Details):
	with open(Path, "w") as File:
		json.dump(Details, File)
		

if __name__ == "__main__":
	main()
