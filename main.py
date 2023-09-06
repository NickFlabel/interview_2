import utils
import db
import dotenv
import os

dotenv.load_dotenv()

DOMAINS_TABLE_NAME = os.getenv('DOMAINS_TABLE_NAME')
RULES_TABLE_NAME = os.getenv('RULES_TABLE_NAME')

data_processor = utils.DataProcessor(DOMAINS_TABLE_NAME)
data_processor.process_data()

data_inserter = utils.DataInserter(data_processor.regex, RULES_TABLE_NAME)
data_inserter.save_data()
