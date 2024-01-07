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
			DisplayImage(Details["FilePath"])
	except FileNotFoundError:
		st.write("User Not Found")

def download_directory(directory_path):
	with zipfile.ZipFile("download.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
		for root, folders, files in os.walk(directory_path):
			for file in files:
				file_path = os.path.join(root, file)
				zipf.write(file_path)
	st.download_button(
        label="Download Directory",
        data="download.zip",
        file_name="Data.zip",
        mime="application/zip"
    	)
#download_directory("Files")


def DisplayImage(path):
	df = pd.read_excel(path)
	st.dataframe(df)
	for index, row in df.iterrows():
		text = row["FORMULA_IN_LATEX"]
		ImgPath = row["IMAGE_FILE_PATH"]

		st.latex(text)
		st.image(ImgPath)
