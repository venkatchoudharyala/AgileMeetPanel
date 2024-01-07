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
	MPath = st.selectbox("Users", dir)
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
	with open("UnVerified.uv", "r") as File:
		NewUsers = json.load(File)
	for i in range(0, len(NewUsers["Names"])):
		st.write(NewUsers["Names"][i])
		Role = st.selectbox("Select Role", ["Member", "Lead"])
		if st.button("Verify"):
			Name = NewUsers["Names"][i]
			del NewUsers["Names"][i]
			with open("LoginApp/UnVerified.uv", "w") as File:
				json.dump(NewUsers, File)
			Path = "UserAcc/" + Name + ".ua"
			with open(Path, "w") as File:
				UDetails = json.load(File)
				UDetails["Role"] = Role
				UDetails["AccVerifStatus"] = "Verified"
				json.dump(UDetails, File)
