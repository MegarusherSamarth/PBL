import re # Imported Regex
import sys
from collections import defaultdict

class LexicalAnalyzer:
    def __init__(self):
        self.line_number = 1
        self.cBrac = 0
        self.nc = 0  # Nested comment counter
        self.flag = False  # Nested comment flag
        self.cLine = 0  # Comment line counter
        self.var = 0  # Variable counter for symbol table
        self.symbol_table = []
        self.constants_table = []
        self.parsed_table = []
        self.comments = []
        self.single_line_comments = []
        
        # Define token patterns
        self.patterns = [
            # Preprocessor directives
            (r'^#.*', 'd', "Preprocessor Statement"),
            
            # Keywords
            (r'\b(auto|break|case|char|const|continue|default|do|else|double|enum|extern|float|for|goto|if|int|long|register|return)\b', 
             'k', "Keyword"),
            
            # Data types with modifiers
            (r'\b(signed|unsigned)?\s*(long|short)?\s*(int|char|void)\b', 
             'k', "Keyword"),
            
            # Functions
            (r'\b(signed|unsigned)?\s*(long|short)?\s*(int|char|void)\s*([a-zA-Z_]\w*)\s*\(.*\)', 
             'j', "Procedure"),
            
            # Arrays
            (r'([a-zA-Z_]\w*)\s*\[\s*\d*\s*\]', 
             'a', "Array"),
            
            # Pointers
            (r'\*\s*([a-zA-Z_]\w*)', 
             'q', "Pointer"),
            
            # Identifiers
            (r'[a-zA-Z_]\w*', 
             'i', "Identifier"),
            
            # Operators
            (r'[><]=?|!=|==', 'r', "Relational Op"),
            (r'[&|^~]', 'l', "Logical Op"),
            (r'[+\-*/%]', 'o', "Arithmetic Op"),
            (r'=', 'e', "Assignment Op"),
            
            # Punctuation
            (r'[(){}\[\];,.:]', 'p', "Punctuator"),
            
            # Constants
            (r'\d+', 'c', "Integer Constant"),
            (r'[-+]?\d*\.\d+([eE][-+]?\d+)?', 'f', "Float Constant"),
            (r'\'.\'', 'z', "Character Constant"),
            (r'\"(\\.|[^"\\])*\"', 's', "String Literal"),
            
            # Comments
            (r'//.*', 'COMMENT', None),
            (r'/\*', 'MULTILINE_COMMENT_START', None),
            (r'\*/', 'MULTILINE_COMMENT_END', None),
            
            # Whitespace
            (r'\s+', None, None),
            
            # Newlines
            (r'\n', 'NEWLINE', None)
        ]
        
        # Compile regex patterns
        self.compiled_patterns = []
        for pattern, token_type, token_name in self.patterns:
            self.compiled_patterns.append((re.compile(pattern), token_type, token_name))
    
    def analyze(self, code):
        self.code = code
        self.pos = 0
        self.length = len(code)
        
        while self.pos < self.length:
            self.match_patterns()
    
    def match_patterns(self):
        for pattern, token_type, token_name in self.compiled_patterns:
            match = pattern.match(self.code, self.pos)
            if match:
                self.handle_match(match, token_type, token_name)
                return
        
        # No pattern matched - invalid character
        char = self.code[self.pos]
        print(f"{self.input_file} : {self.line_number} : Invalid character '{char}'")
        self.pos += 1
    
    def handle_match(self, match, token_type, token_name):
        value = match.group()
        start_pos = match.start()
        end_pos = match.end()
        
        # Handle newlines
        if token_type == 'NEWLINE':
            self.line_number += 1
            self.pos = end_pos
            return
        
        # Handle comments
        if token_type == 'COMMENT':
            self.handle_single_line_comment(value)
            self.pos = end_pos
            return
        
        if token_type == 'MULTILINE_COMMENT_START':
            self.handle_multiline_comment_start()
            self.pos = end_pos
            return
        
        if token_type == 'MULTILINE_COMMENT_END':
            self.handle_multiline_comment_end()
            self.pos = end_pos
            return
        
        # Skip whitespace
        if token_type is None:
            self.pos = end_pos
            return
        
        # Handle braces
        if value == '{':
            self.cBrac += 1
        elif value == '}':
            self.cBrac -= 1
        
        # Insert to tables if not in comment
        if self.nc <= 0:
            self.insert_to_tables(value, token_type, token_name)
        
        self.pos = end_pos
    
    def handle_single_line_comment(self, comment):
        # Remove the // prefix
        comment_content = comment[2:]
        self.single_line_comments.append(comment_content)
        self.comments.append(f"//{comment_content}")
    
    def handle_multiline_comment_start(self):
        self.nc += 1
        self.cLine += 1
        if self.nc > 1:
            print(f"{self.input_file} : {self.line_number} : Nested Comment")
            self.flag = True
    
    def handle_multiline_comment_end(self):
        if self.nc > 0:
            self.nc -= 1
        else:
            print(f"{self.input_file} : {self.line_number} : */ found before /*")
        
        if self.nc == 0:
            # End of multiline comment
            pass
    
    def insert_to_tables(self, value, token_type, token_name):
        # Check if this token already exists in symbol table
        existing_entry = None
        for entry in self.symbol_table:
            if entry['lexeme'] == value:
                existing_entry = entry
                break
        
        if existing_entry is None:
            # Add to symbol table
            if token_type in ['i', 'a', 'q', 'j']:  # Identifiers, arrays, pointers, functions
                entry = {
                    'lexeme': value,
                    'type': token_name,
                    'attribute_value': self.var,
                    'line_number': self.line_number
                }
                self.symbol_table.append(entry)
                self.var += 1
            
            # Add to constants table
            if token_type in ['c', 'f', 'z']:  # Constants
                const_type = {
                    'c': 'int',
                    'f': 'float',
                    'z': 'char'
                }.get(token_type)
                
                entry = {
                    'lexeme': value,
                    'type': const_type,
                    'attribute_value': self.var,
                    'line_number': self.line_number
                }
                self.constants_table.append(entry)
                self.var += 1
        
        # Add to parsed table
        entry = {
            'lexeme': value,
            'type': token_name,
            'attribute_value': self.var - 1 if existing_entry is None else existing_entry['attribute_value'],
            'line_number': self.line_number
        }
        self.parsed_table.append(entry)
    
    def generate_reports(self):
        # Generate symbol table report
        symbol_report = "\nSymbol Table:\n"
        symbol_report += f"{'Lexeme':20}{'Type':30}{'Attribute Value':30}{'Line Number':15}\n"
        for entry in self.symbol_table:
            symbol_report += f"{entry['lexeme']:20}{entry['type']:30}{entry['attribute_value']:30}{entry['line_number']:15}\n"
        
        # Generate constants table report
        constants_report = "\nConstants Table:\n"
        constants_report += f"{'Lexeme':20}{'Type':30}{'Attribute Value':30}{'Line Number':15}\n"
        for entry in self.constants_table:
            constants_report += f"{entry['lexeme']:20}{entry['type']:30}{entry['attribute_value']:30}{entry['line_number']:15}\n"
        
        # Generate parsed table report
        parsed_report = "\nParsed Table:\n"
        parsed_report += f"{'Lexeme':20}{'Type':30}{'Attribute Value':30}{'Line Number':15}\n"
        for entry in self.parsed_table:
            parsed_report += f"{entry['lexeme']:20}{entry['type']:30}{entry['attribute_value']:30}{entry['line_number']:15}\n"
        
        # Generate comments report
        comments_report = "\nComments:\n"
        if self.flag:
            comments_report += f"Nested Comments ({self.cLine} lines)\n"
        else:
            comments_report += f"Multi-line Comments ({self.cLine} lines):\n"
            comments_report += "\n".join(self.comments) + "\n"
            comments_report += "\nSingle-line Comments:\n"
            comments_report += "\n".join(self.single_line_comments) + "\n"
        
        return {
            'symbol_table': symbol_report,
            'constants_table': constants_report,
            'parsed_table': parsed_report,
            'comments': comments_report
        }
    
    def analyze_file(self, file_path):
        self.input_file = file_path
        with open(file_path, 'r') as f:
            code = f.read()
        
        self.analyze(code)
        
        # Check for unclosed comments
        if self.nc != 0:
            print(f"{self.input_file} : {self.line_number} : Comment Does Not End")
        
        # Check for unbalanced braces
        if self.cBrac != 0:
            print(f"{self.input_file} : {self.line_number} : Unbalanced Parentheses")
        
        return self.generate_reports()

def main():
    if len(sys.argv) > 1:
        lexer = LexicalAnalyzer()
        reports = lexer.analyze_file(sys.argv[1])
        
        # Write reports to files
        with open('symbolTable.txt', 'w') as f:
            f.write(reports['symbol_table'])
        
        with open('constantTable.txt', 'w') as f:
            f.write(reports['constants_table'])
        
        with open('parsedTable.txt', 'w') as f:
            f.write(reports['parsed_table'])
            f.write("\n\n" + reports['comments'])
        
        print("Lexical analysis completed. Reports generated in:")
        print("- symbolTable.txt")
        print("- constantTable.txt")
        print("- parsedTable.txt")
    else:
        print("Usage: python lexer.py <input_file>")

if __name__ == "__main__":
    main()
