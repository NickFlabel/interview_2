import db
import re
import dotenv
import os

dotenv.load_dotenv()

NUMBER_OF_DOMAINS = os.getenv('NUMBER_OF_DOMAINS')

class DataProcessor:
    project_patterns = None
    parsed_data = None
    regex = None
    number_of_domains = int(NUMBER_OF_DOMAINS)


    def __init__(self, table_name: str, database_manager = db.DatabaseManager):
        self.table_name = table_name
        self.database_manager = database_manager
        self.regex = {}

    def process_data(self):
        self._extract_data()
        for project, list_of_domains in self.project_patterns.items():
            self._parse_data(list_of_domains)
            self._get_positions()
            self.regex[project] = self._construct_regex()

    def _extract_data(self):
        self.extracted_data = self.database_manager(self.table_name).get_data()
        self.project_patterns = {}
        for project_id, domain in self.extracted_data:
            self.project_patterns.setdefault(project_id, [])
            self.project_patterns[project_id].append(domain)

    def _parse_data(self, list_of_domains: list):
        seen = {}
        for domain in list_of_domains:
            parts = reversed(domain.split('.'))
            for i, part in enumerate(parts):
                if part not in seen:
                    seen[part] = [i, 1]
                else:
                    seen[part][1] += 1
        self.parsed_data = seen

    def _get_positions(self):
        positions = {}
        for key, position in self.parsed_data.items():
            positions.setdefault(position[0], [])
            positions[position[0]].append(key)

        self.positions = positions

    def _construct_regex(self):
        self._filter_by_length()
        
        regex = r''
        for key in self.number_of_domains_by_length.keys():
            if len(self.number_of_domains_by_length[key]) > self.number_of_domains:
                if regex:
                    regex += r'|'  
                regex += r'^((?=(?:' + r'\D*\d){1,' + re.escape(str(key)) + '}\D*).{' + re.escape(str(key)) + r'}' + r'\..+)'

        return regex
    

    def _filter_by_length(self):
        pos_dict = {}
        for key in self.positions.keys():
            for position in self.positions[key]:
                if re.match(r'.*\d.*', position):
                    pos_dict.setdefault(len(position), [])
                    pos_dict[len(position)].append(position)

        self.number_of_domains_by_length = pos_dict


class DataInserter:

    def __init__(self, regex: dict, table_name: str, database_manager = db.DatabaseManager) -> None:
        self.regex = regex
        self.table_name = table_name
        self.database_manager = database_manager
        self.data = []

    def save_data(self):
        self._prepare_data()
        for values in self.data:
            res = self.database_manager(self.table_name).save_data(values)

    def _prepare_data(self):
        for key in self.regex:
            self.data.append((key, self.regex[key]))