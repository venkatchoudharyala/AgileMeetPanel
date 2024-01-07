import streamlit as st
import json
import zipfile
import os
import pandas as pd
import base64
import io
from PIL import Image
import numpy as np

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
	MPath = st.selectbox("Users", dir, key = "AdminP")
	#UserName = Form.text_input("User Name")
	Path = "UserAcc/" + MPath
	Rapo(Path)
def Rapo(Path):
	try:
		with open(Path, "r") as File:
			UDetails = File.read()
			Details = json.loads(UDetails)
			st.write(Details)
	except FileNotFoundError:
		st.write("User Not Found")
	with open("LoginApp/UnVerified.uv", "r") as File:
		NewUsers = json.load(File)
	if len(NewUsers["Names"]) != 0:
		st.write(NewUsers["Names"][0])
		Role = st.selectbox("Select Role", ["Member", "Lead"], index = None, key = NewUsers["Names"][0])
		if st.button("Verify"):
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
		if st.button("Suspend"):
			with open("LoginApp/UnVerified.uv", "r") as File:
				UDetails = json.load(File)
			with open("LoginApp/UnVerified.uv", "w") as File:
				del NewUsers["Names"][0]
				json.dump(NewUsers, File)
		
