# Domain regex generator

To run this script you must perform the following:

1) Clone the repository

```bash
git clone https://github.com/NickFlabel/interview_2.git
```

2) Install the requirements:

```bash
pip install -r requirements.txt
```

3) Change the settings in .env file. For convinience I included my own .env file. 

- DATABASE: relative path to the sqllite3 database with relevant data
- NUMBER_OF_DOMAINS: number of domains of similar length which is used by the script to filter the invalid domains. I.e. if there is only <NUMBER_OF_DOMAINS> domains of a given length the script will not generate the regexp for this length.
- DOMAINS_TABLE_NAME: name of the table which contains project_id and domain name 
- RULES_TABLE_NAME: name of the table which contains project_id and regexp for a given rule

4) Run the script: 

```bash
python3 main.py
```

5) If you desire you may also run one test:

```bash
pytest
```
