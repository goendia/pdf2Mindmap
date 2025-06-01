import json

class PDF2MindMapper():
    """
    Extracts text from a Docling-like JSON file and indents it based on the 'left' coordinate.
    Handles nested bullet points by increasing indentation levels.

    Args:
        json_file_path (str): Path to the JSON file.
        indent_size (int): The number of spaces for each indentation level.

    Returns:
        str: A string with the extracted and indented text.  Returns an error message if the file can't be opened or parsed.
    """
    def __init__(self, jsonFilePath, indentSize=4):
        self.jsonFilePath = jsonFilePath
        self.indentSize = indentSize
        self.data = {}   # The JSON data
        self.output = ""
        self.previousLeft = 0  # Keep track of the previous left coordinate
        self.indentLevel = 0 # The current indentation level
        self.indentSize = 1   # The number of spaces to indent each level. 
        self.currentText = ""

    def openPDF(self):
            try:
                with open(self.jsonFilePath, 'r', encoding='utf-8') as f:  # Important: Specify encoding
                    self.data = json.load(f)
            except FileNotFoundError:
                return f"Error: File not found at {self.jsonFilePath}"
            except json.JSONDecodeError:
                return f"Error: Invalid JSON format in {self.jsonFilePath}"
    
    def extractIndentLevel(self):
        # TODO: Implement this
        return
    
    def filterContent(self):
        # Filter unneeded data like page numbers, header data, footing, etc
        return

    def process(self):
        text_items = self.data['texts']

        for element in text_items:
            self.currentText = element['text'].strip()
            # Determine indentation level based on left coordinate
            self.currentLeft = element['prov'][0]['bbox']['l']
            # Skip empty text items and bullet points that are not nested
            if len(self.currentText) == 0 or self.currentText== 'https://www.DionTraining.com' or self.currentText == 'CompTIA Network+ (N10-009) (Study Notes)' or self.currentLeft > 500:
                continue

            # Determine indentation level based on left coordinate
            if self.currentLeft > self.previousLeft:
                self.indentLevel += 1   # Increase indent for nested items
            elif self.currentLeft < self.previousLeft:
                self.indentLevel -= 1 # Decrease indent, but not below 0

            indentation = " " * (self.indentLevel * self.indentSize)
            self.output += f"{indentation}{self.currentText}\n"
            self.previousLeft = self.currentLeft
        return self.output

    # Print to console
    def printToConsole(self):
        print(self.output)

    def saveToFile(self, file_path, indented_text):
        try:
            with open(file_path, "w", encoding="utf-8") as outfile:
                outfile.write(indented_text)
        except:
            print("Error saving file.")



# Example Usage:
file_path = "/home/chris/Documents/Udemy/CompTIA-Network/studyguide1-50.json"  # Replace with your file path
pdf2map = PDF2MindMapper(file_path)
pdf2map.openPDF()
pdf2map.process()
pdf2map.printToConsole()