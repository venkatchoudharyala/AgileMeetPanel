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
import Emailer

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
				tab1, tab2, tab3, tab4 = st.tabs(["Projects", "New Project", "Meetings", "New Meeting"])
				with tab1:
					LeadPanel()
				with tab2:
					CreateProject()
				with tab3:
					MeetingPanel()
				with tab4:
					Projects = UserDetails["Projects"]
					project = st.selectbox("Select a Project", Projects, index = None, key = "p")
					if project != None:
						k = os.listdir("MeetingNotes/" + ProjName)
						CreateMeetSession(project, len(k))
					
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
				newRow = pd.DataFrame({"Task": Tasks[SelMem][i]["Task"], "Status": Tasks[SelMem][i]["Status"], "Deadline": Tasks[SelMem][i]["Deadline"]}, index=[i])
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
				newRow = pd.DataFrame({"Task": Tasks[SelMem][i]["Task"], "Status": Tasks[SelMem][i]["Status"], "Deadline": Tasks[SelMem][i]["Deadline"]}, index=[i])
				df = pd.concat([df, newRow], ignore_index = True)
			st.dataframe(df)

	with st.form(key = "mem", clear_on_submit = True):
		Tasks = []
		for i in UserDetails["Tasks"]:
			if i["Status"] != "Solved":
				NewRow = "Ticket - " + i["Task"] + ", Project: " + i["Project"]
				Tasks.append(NewRow)
		SelTask = st.selectbox("Update your Work", Tasks)
		ind = Tasks.index(SelTask)
		TicketStatus = st.selectbox("Select Ticket Status", ["In Progress", "Solved", "Blocked"])
		if st.form_submit_button("Update"):
			Details = FileReader("UserAcc/" + UserDetails["Name"] + ".ua")
			Details["Tasks"][ind]["Status"] = TicketStatus
			FileWriter("UserAcc/" + UserDetails["Name"] + ".ua", Details)

			Details = FileReader("Projects/" + UserDetails["Tasks"][ind]["Project"] + ".pjs")
			STitles = []
			for j in Details["SessionTitles"]:
				STitles.append(j["Title"])
			PjIndex = STitles.index(UserDetails["Tasks"][ind]["MeetSession"])
			TaskInd = []
			for j in Details["MeetSessions"][PjIndex]["Tasks"][UserDetails["Name"] + ".ua"]:
				TaskInd.append(j["Task"])
			SpectaskIndex = TaskInd.index(UserDetails["Tasks"][ind]["Task"])
			Details["MeetSessions"][PjIndex]["Tasks"][UserDetails["Name"] + ".ua"][SpectaskIndex]["Status"] = TicketStatus
			FileWriter("Projects/" + UserDetails["Tasks"][ind]["Project"] + ".pjs", Details)

			st.success("Ticket Status Updated Successfully", icon = "✅")

def CreateProject():
	with st.form(key = "cp", clear_on_submit=True):
		ProjName = st.text_input("Enter the Project Name")
		ProjDescp = st.text_input("Description")
	
		dirs = os.listdir("UserAcc")
		dirs.remove("Admin.ua")
		dirs.remove(UserDetails["Name"] + ".ua")
		dirs.remove("Test.ua")
		Team = st.multiselect("Select Team", dirs, placeholder = "Select ur Team Members")
		Team.append(UserDetails["Name"] + ".ua")
		if st.form_submit_button("Create"):
			os.makedirs("MeetingNotes/" + ProjName)
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
				Message = "Project - " + ProjName + " Created Successfully, Please reload the Application to Connect with your Team!!"
				st.success(Message, icon="✅")
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
			if len(SessionTitles) != 0:
				SelMeet = st.selectbox("Select a Past Meeting", SessionTitles, index = len(SessionTitles)-1)
			else:
				st.write("No Meet Sessions yet")
			if len(SessionTitles) != 0 and SelMeet:
				ProjectMeetFile = ProjectMeetFile + "/" + SelMeet
				st.subheader("Meeting Notes")
				with open(ProjectMeetFile, "r") as file:
					lines = file.readlines()
					for line in lines:
						st.write(line.strip())
	
				SelMeetInd = SessionTitles.index(SelMeet)
				#st.write(SelMeetInd)
				#st.write(PjDetails["MeetSessions"])
				SelMem = st.selectbox("Select a Team Member", list(PjDetails["MeetSessions"][SelMeetInd]["Tasks"].keys()), key = "TM")
				try:
					SelMemTasks = PjDetails["MeetSessions"][SelMeetInd]["Tasks"][SelMem]
					df = pd.DataFrame(columns = ["Task", "Status", "Deadline"])
					for i in range(0, len(SelMemTasks)):
						newRow = pd.DataFrame({"Task": SelMemTasks[i]["Task"], "Status": SelMemTasks[i]["Status"], "Deadline": SelMemTasks[i]["Deadline"]}, index=[i])
						df = pd.concat([df, newRow], ignore_index = True)
					st.dataframe(df)
				except KeyError:
					st.write("No Tasks Assigned")

def CreateMeetSession(ProjName, len):
	Path = "Projects/" + ProjName + ".pjs"
	PjDetails = FileReader(Path)
	NewMeetID = len(PjDetails["SessionTitles"])
	if 'clicked' not in st.session_state:
    		st.session_state.clicked = False
	with st.form(key = "fomr", clear_on_submit=True):
		time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
		st.session_state["Title"] = st.text_input("Enter a Title for the Note or Leave blank for Automated title")
		if st.form_submit_button("Create"):
			click_button()
			if st.session_state["Title"] == "":
				st.session_state["Title"] = "MEET_SESSION_ID_" + str(len)
				#st.session_state["Title"] = st.session_state["Title"] + ".txt"
			if st.session_state["Title"] == "":
				kpr = "MEET_HELD_ON_" + str(time.timestamp()).replace(".", "_")
			else:
				kpr = st.session_state["Title"]
			with open("MeetingNotes/" + ProjName + "/" + kpr, "w") as file:
    				file.write("Session Name: " + st.session_state["Title"] + "\n")
			PjDetails["SessionTitles"].append({"Title": st.session_state["Title"], "TimeStamp": str(time)})
			PjDetails["MeetSessions"].append({"Tasks": {}})
			FileWriter(Path, PjDetails)
			if st.session_state.clicked:
				st.success("Meeting Created Successfully just Work on with the Meet Notes", icon="✅")
	Note = st.text_area("Enter Action Items or Meeting Notes")
	col1, col2 = st.columns(2)
	with col1:
		Team = PjDetails["Team"]
		SelMem = st.selectbox("Select a Team Member", Team)
		DeadLine = st.date_input("Select the Deadline", value = "today")
		Status = "Un Resolved"


	with col2:
		st.title(" ")

		if st.button("Assign"):
			timers = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
			PjDetails = FileReader(Path)
			if SelMem not in PjDetails["MeetSessions"][-1]["Tasks"].keys():
				PjDetails["MeetSessions"][-1]["Tasks"][SelMem] = []
			PjDetails["MeetSessions"][-1]["Tasks"][SelMem].append({"Task": Note, "Status": Status, "Deadline": str(DeadLine)})
			PjDetails["Tasks"][SelMem].append({"Task": Note, "Status": Status, "Deadline": str(DeadLine)})
			FileWriter(Path, PjDetails)
			if st.session_state["Title"] == "":
				kpr = "MEET_HELD_ON_" + str(time.timestamp()).replace(".", "_")
			else:
				kpr = st.session_state["Title"]
			with open("MeetingNotes/" + ProjName + "/" + kpr, "a") as file:
				file.write("\n--- New Note ---\n")
				file.write("Task Assigned to " + SelMem + "\n")
				file.write("Time Stamp: " + str(timers) + "\n")
				file.write("Notes: " + Note)

			subject = ProjName + ", New Task, " + "Deadline: " + str(DeadLine) 
			body = Note
			RecDetails = FileReader("UserAcc/" + SelMem)
			NewRow = {"Project": ProjName, "MeetSession": kpr, "Task": Note, "Status": Status, "Deadline": str(DeadLine)}
			RecDetails["Tasks"].append(NewRow)
			FileWriter("UserAcc/" + SelMem, RecDetails)
			to_email = RecDetails["Email"]
			smtp_server = "smtp.gmail.com"
			smtp_port = 587
			smtp_user = "vsoft101@gmail.com"  # Replace with your Gmail email address
			smtp_password = "hfvq iubg yhhr ygca"  # Replace with your Gmail app password
			Emailer.send_email(subject, body, to_email, smtp_server, smtp_port, smtp_user, smtp_password)

		if st.button("Save & New Note"):
			timers = str(datetime.datetime.now(pytz.timezone("Asia/Kolkata")))
			if st.session_state["Title"] == "":
				kpr = "MEET_HELD_ON_" + str(time.timestamp()).replace(".", "_")
			else:
				kpr = st.session_state["Title"]
			with open("MeetingNotes/" + ProjName + "/" + kpr, "a") as file:
				file.write("\n--- New Note ---\n")
				file.write("Time Stamp: " + str(timers) + "\n")
				file.write("Notes: " + Note)

def click_button():
    st.session_state.clicked = True
			
				
def FileReader(Path):
	with open(Path, "r") as File:
		PjDetails = json.load(File)
	return PjDetails

def FileWriter(Path, Details):
	with open(Path, "w") as File:
		json.dump(Details, File)
		

if __name__ == "__main__":
	main()
