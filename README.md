# resumeranking 

Extract the text from resume formats like docx,doc,rtf,txt and pdf

1. We are extracting experience from extract_exp.py.
2. Extract Emal, Phone no from ExtractEntities.py file.
3. Extract Skills and non technical skills from getCategory.py file.
4. Run app.py from CMD as it is an web app built on Flask Framework of Python.

We are giving weightage to each resume in 4 ways as mentioned below:

1. 40% weightage to Experience matching of Resume to JD
2. 40% Weightage of Skill in Resume to JD matching
3. 15% weightage of JD to Resume matching using Cosine Distance
4. 5% weightage of Non-Technical skill matching of Resume to JD

All above weightages can be easily changed from the coding. 
We can also seperately create a config file to make it more flexible.

Software
Gensim
Numpy==1.11.3
Pandas
Sklearn
PdfMiner.six
Python 3.6.0 |Anaconda 4.3.0 (64-bit)|

Dependencies:
Must have textract installed   
To install refer: You can now go to https://github.com/deanmalmgren/textract/releases and download v1.6.2 which provides only requirement updates over v1.6.1 (fixing the unicode debug error) or v1.6.3 which is the latest (as of writing this.)

Once downloaded, extract, cd [folder extracted to] and pip install .

Note: Just keep in mind there is always the concern that as requirements are updated malicious code can be inserted into dependencies and update this at your own risk.

Running
Simply run this command from root directory.
python app.py
