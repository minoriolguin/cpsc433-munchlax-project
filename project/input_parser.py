# CPSC 433 - Artificial Intelligence - Fall 2024
# Aditi Yadav
# Jaden Myers
# Minori Olguin
# Monica Nguyen
# Thi Ngoc Anh Nguyen

class InputParser:
    
    def __init__(self):
        self.data = {
            "Name": "",
            "Game slots": [],
            "Practice slots": [],
            "Games": [],
            "Practices": [],
            "Not compatible": [],
            "Unwanted": [],
            "Preferences": [],
            "Pair": [],
            "Partial assignments": []
        }

    def get_file_name():
        filename = input("Enter filename: ").strip()
        return filename

    def parse_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    
                    if not line:
                        continue
                    

                    

                
        
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"error: {e}")
            

def main():
    parser = InputParser()
    filename = parser.get_file_name()
    parser.parse_file(filename)

    
if __name__ == "__main__":
    main()
