import json
# from docling.document_converter import DocumentConverter
import re
from operator import itemgetter

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
        self.indentSize = indentSize# The number of spaces to indent each level
        self.data = {}   # The JSON data
        self.output = ""
        self.previousLeft = 0  # Keep track of the previous left coordinate
        self.indentLevel = 0 # The current indentation level
        self.currentText = ""

    # def convertPDF(self, filePath):
    #     source = filePath  # PDF path or URL
    #     converter = DocumentConverter()
    #     result = converter.convert(source)
    #     result_dict = result.document.export_to_dict()
    #     print(json.dumps(result_dict, indent=2))

    def openJSON(self):
            try:
                with open(self.jsonFilePath, 'r', encoding='utf-8') as f:  # Important: Specify encoding
                    self.data = json.load(f)
            except FileNotFoundError:
                return f"Error: File not found at {self.jsonFilePath}"
            except json.JSONDecodeError:
                return f"Error: Invalid JSON format in {self.jsonFilePath}"
    
    def extractIndentLevels(self, sortType="items"):
        listOfIndentLevels = {}
        for element in self.data['texts']:
            currentLeft = element['prov'][0]['bbox']['l']
            if currentLeft in listOfIndentLevels:
                listOfIndentLevels[currentLeft] += 1
            else:
                listOfIndentLevels[currentLeft] = 1
        if sortType == "items":
            sortedlistOfIndentLevels = dict(sorted(listOfIndentLevels.items()))
        elif sortType == "values":
            sortedlistOfIndentLevels = dict(sorted(listOfIndentLevels.items(), key=itemgetter(1), reverse=True))
        else:
            return f"Error: Invalid sortType {sortType}"
        return sortedlistOfIndentLevels

    def findLikelyListBullets(self, text):
        # Define a regular expression that matches potential bullet characters.
        bullet_regex = r"[\u2022\u2043\u25e6\u25cf\u25cb\u25aa\u25ab\u25ac\u25a0\u25ad\u2047\u203a\u203b\u203c\u203d\u276f\u2770\u30fb\ufe30\uff08\uff09]"
        matches = re.findall(bullet_regex, text)
        # Convert the list of matches to a set to remove duplicates.
        bullets = set(matches)
        unlikely_bullets = {
            # Add characters here that your analysis shows are commonly
            # matched but *aren't* actually list bullets in *your* document.
            # Example:
            # '\ufe30' # A common bullet point, but might also appear in other contexts
        }
        filtered_bullets = bullets #- unlikely_bullets

        return filtered_bullets
    
    def findBulletIndentationLevels(self):
        # This function uses the likely list bulletts to determine the indentation level of the bullets
        bulletCharacters = self.findLikelyListBullets(self.output)
        listOfIndentLevels = {}
        # Add 1 to each indent level for each instance of the bullet character.
        # This is a bit tricky because we need to check the first character of each text block.
        # If it's a bullet character then we add one, otherwise we ignore that text block.
        for element in self.data['texts']:
            firstTextSymbol = element['text'][0].strip()
            currentLeft = element['prov'][0]['bbox']['l']
            if firstTextSymbol not in bulletCharacters:
                continue
            elif firstTextSymbol in bulletCharacters:
                if firstTextSymbol in listOfIndentLevels and currentLeft in listOfIndentLevels[firstTextSymbol]:
                    listOfIndentLevels[firstTextSymbol][currentLeft] += 1
                elif firstTextSymbol in listOfIndentLevels and currentLeft not in listOfIndentLevels[firstTextSymbol]:
                    listOfIndentLevels[firstTextSymbol].update({currentLeft : 1})
                else:
                    listOfIndentLevels[firstTextSymbol] = {currentLeft : 1}

        return listOfIndentLevels

    def extractIndentedText(self):
        # TODO: Implement this
        return
    
    def filterContent(self):
        # Filter unneeded data like page numbers, header data, footing, etc
        return

    def skipItem(self):
        # Skip empty text items, header and footer, etc
        if len(self.currentText) == 0 or self.currentText== 'https://www.DionTraining.com' or self.currentText == 'CompTIA Network+ (N10-009) (Study Notes)' or self.currentLeft > 500:
            return True
        return False

    def process(self):
        text_items = self.data['texts']

        for element in text_items:
            self.currentText = element['text'].strip()
            # Determine indentation level based on left coordinate
            self.currentLeft = element['prov'][0]['bbox']['l']
            if self.skipItem():
                continue

            # Determine indentation level based on left coordinate
            match self.currentLeft:
                case 90:
                    self.indentLevel = 0
                case 126:
                    self.indentLevel = 1
                case 162:
                    self.indentLevel = 2
                case 198 | 198.158:
                    self.indentLevel = 3
                case 234:
                    self.indentLevel = 4
                case 270:
                    self.indentLevel = 5
                case 306 | 306.072:
                    self.indentLevel = 6
                case 342:
                    self.indentLevel = 7
                case _:
                    self.indentLevel = 0
            # if self.currentLeft > self.previousLeft:
            #     self.indentLevel += 1   # Increase indent for nested items
            # elif self.currentLeft < self.previousLeft:
            #     self.indentLevel -= 1 # Decrease indent, but not below 0

            indentation = " " * (self.indentLevel * self.indentSize)
            self.output += f"{indentation}{self.currentText}\n"
            self.previousLeft = self.currentLeft
        return self.output

    # Print to console
    def printToConsole(self):
        print(self.output)

    def cleanOutput(self):
        # Normalize the text and remove non-printable characters
        self.output = re.sub(r'\u25cf ', '', self.output)
        self.output = re.sub(r'\u25cb ', '', self.output)
        self.output = re.sub(r'\u25a0 ', '', self.output)
        return self.output

    def saveToFile(self, filePath, indentedText):
        try:
            with open(filePath, "w", encoding="utf-8") as outFile:
                outFile.write(indentedText)
        except:
            print("Error saving file.")



# Example Usage:
# file_path = "/home/chris/Documents/Udemy/CompTIA-Network/studyguide1-50.json"  # Replace with your file path
filePath = "/home/chris/Documents/Udemy/CompTIA-Network/CompTIANetworkN10-009StudyGuide.json"  # Replace with your file path
pdf2map = PDF2MindMapper(filePath)
# pdf2map.convertPDF("/home/chris/Documents/Udemy/CompTIA-Network/1_DOCLING_CompTIA+Network++(N10-009)+Study+Guide.pdf")
pdf2map.openJSON()
pdf2map.process()
print(pdf2map.findLikelyListBullets(pdf2map.output))
# pdf2map.cleanOutput()
# pdf2map.printToConsole()
print(pdf2map.findBulletIndentationLevels())
print(pdf2map.extractIndentLevels(sortType="values"))
# pdf2map.saveToFile("/home/chris/Documents/Udemy/CompTIA-Network/CompTIANetworkN10-009StudyGuide.txt", pdf2map.output)