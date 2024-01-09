import streamlit as st
import json
import os
import pandas as pd
import datetime
import Emailer


st.set_page_config(initial_sidebar_state = "collapsed")

hide_st_style = """
		<style>
		header {visibility: hidden;}
		footer {visibility: hidden;}
  		</style>
  		"""

st.markdown(hide_st_style, unsafe_allow_html = True)

def Scrapper():
	Form = st.form("Login")
	dir = os.listdir("UserAcc")
	PrDir = os.listdir("Projects")
	PrDir.remove("test.pjs")
	dir.remove("Test.ua")
	col1, col2, col3 = st.columns(3)
	with st.expander("Users"):
		MPath = st.selectbox("Users", dir, key = "AdminP", label_visibility = "collapsed")
		Path = "UserAcc/" + MPath
		Details = Rapo(Path)
		OverDue = []
		for i in Details["Tasks"]:
			# %H:%M:%S.%f+05:30
			DeadLine = datetime.datetime.strptime(i["Deadline"], '%Y-%m-%d')
			if i["Status"] != "Solved" and TimeDelta(datetime.datetime.now(), DeadLine):
				st.error("Task: " + i["Task"] + " of the Project, " + i["Project"] + " Was crossed DeadLine")
				OverDue.append(i)	
			elif i["Status"] != "Solved":
				st.success("Task: " + i["Task"] + " of the Project, " + i["Project"] + " is still Pending")
		if len(OverDue) > 0:
			if st.button("Send OverDue Remainder"):
				for i in OverDue:
					OverDewMailer(i, Details["Email"])
				st.success("Over Due Remainder Sent")
		else:
			st.success(Details["Name"] + " is upto date", icon="✅")
	with st.expander("Projects"):
		PPath = st.selectbox("Projects", PrDir, key = "PP", label_visibility = "collapsed")
		if PPath:
			Path = "Projects/" + PPath
			Rapo(Path)
	with st.expander("Authorizations"):
		with open("LoginApp/UnVerified.uv", "r") as File:
			NewUsers = json.load(File)
		if len(NewUsers["Names"]) != 0:
			st.error("User Name: " + NewUsers["Names"][0])
			with open("UserAcc/" + NewUsers["Names"][0] + ".ua" , "r") as File:
				k = json.load(File)
			st.error("Email: " + k["Email"])
			Role = st.selectbox("Select Role", ["Member", "Lead"], index = None, key = NewUsers["Names"][0])
			col1, col2 = st.columns(2)
			with col1:
				if st.button("Verify") and Role != None:
					Name = NewUsers["Names"][0]
					del NewUsers["Names"][0]
					with open("LoginApp/UnVerified.uv", "w") as File:
						json.dump(NewUsers, File)
					Path = "UserAcc/" + Name + ".ua"
					with open(Path, "r") as File:
						UDetails = json.load(File)
					with open(Path, "w") as File:
						UDetails["Role"] = Role
						UDetails["AccVerifStatus"] = "Verified"
						json.dump(UDetails, File)
					st.experimental_rerun()
			with col2:
				if st.button("Suspend"):
					with open("LoginApp/UnVerified.uv", "r") as File:
						UDetails = json.load(File)
					with open("LoginApp/UnVerified.uv", "w") as File:
						del NewUsers["Names"][0]
						json.dump(NewUsers, File)
					st.experimental_rerun()
		else:
			st.success("No pending Authorizations left")
	#UserName = Form.text_input("User Name")
	
def Rapo(Path):
	try:
		with open(Path, "r") as File:
			UDetails = File.read()
			Details = json.loads(UDetails)
			st.write(Details)
			return Details
	except FileNotFoundError:
		st.write("User Not Found")
def TimeDelta(Curr, Deadline):
	if Deadline < Curr:
		return True
	else:
		return False
def OverDewMailer(TaskDetail, EmailID):
	subject = TaskDetail["Project"] + ", Task, " + TaskDetail["Task"]
	body = "has crossed DeadLine please report to Admin and Teamlead Immediately" 
	to_email = EmailID
	smtp_server = "smtp.gmail.com"
	smtp_port = 587
	smtp_user = "vsoft101@gmail.com"
	smtp_password = "hfvq iubg yhhr ygca"
	Emailer.send_email(subject, body, to_email, smtp_server, smtp_port, smtp_user, smtp_password)
