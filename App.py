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
					if st.checkbox("Create New Project", value = False):
						CreateProject()
			elif Role == "Member" and Status == "Verified":
				tab1, tab2 = st.tabs(["Projects", "Meetings"])
				with tab1:
					MemberPanel()
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
			SelMem = UserDetails["Name"]
			
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
			
			PjDetails = {"Description": ProjDescp, "MeetSessions": [], "Team": Team, "Tasks": tsks}
			Path = "Projects/" + ProjName.strip() + ".pjs"
			FileWriter(Path, PjDetails)
			Team = []
			st.experimental_rerun()
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
