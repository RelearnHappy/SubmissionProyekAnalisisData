# SubmissionProyekAnalisisData ✨

## File_Structures
```
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
│   └── foto_sepeda.png
├── data
│   ├── day.csv
│   └── hour.csv
├── README.md
├── notebook.ipynb
├── requirements.txt
│── url.txt
```


## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```


## Setup Environment - Shell/Terminal
```
mkdir SubmissionProyekAnalisisData
cd SubmissionProyekAnalisisData
pipenv install
pipenv shell
pip install -r requirements.txt
```


## Run steamlit app
```
streamlit run dashboard.py
```
