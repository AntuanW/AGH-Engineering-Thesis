from .parser import Parser
import re

class InstructionParser(Parser):

    def _read_data(self):
        if not isinstance(self.source, list):
            raise ValueError('Source must be a list of strings')

        if not all(isinstance(item, str) for item in self.source):
            raise ValueError('All items in the source list must be strings')

        self.data = self.source

    def _parse(self):
        skip_patterns = [
            r"^!",
            r"^Building configuration",
            r"^Current configuration.*",
            r"^no service timestamps.*",
            r"^no service password-encryption",
            r"^platform .*",
            r"^redundancy.*",
            r"^diagnostic bootup.*",
            r"^memory free.*",
            r"^vlan internal allocation.*",
            r"^login on-success.*",
            r"^subscriber templating",
            r"^no license.*",
            r"^login$",
            r"^version*",
            r"^license*"
        ]

        # remove unused interfaces
        for i in range(len(self.data) - 1):
            if self.data[i].startswith('interface') and self.data[i + 1] == '!':
                skip_patterns.append(re.escape(self.data[i]))
        if len(self.data) != 0 and self.data[-1].startswith('interface'):
            skip_patterns.append(re.escape(self.data[-1]))

        filtered_data = []
        for line in self.data:
            if not any(re.match(pattern, line) for pattern in skip_patterns):
                filtered_data.append(line)

        self.data = filtered_data
