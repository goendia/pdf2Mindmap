import json

def extract_and_indent(json_file_path, indent_size=4):
    """
    Extracts text from a Docling-like JSON file and indents it based on the 'left' coordinate.
    Handles nested bullet points by increasing indentation levels.

    Args:
        json_file_path (str): Path to the JSON file.
        indent_size (int): The number of spaces for each indentation level.

    Returns:
        str: A string with the extracted and indented text.  Returns an error message if the file can't be opened or parsed.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:  # Important: Specify encoding
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: File not found at {json_file_path}"
    except json.JSONDecodeError:
        return f"Error: Invalid JSON format in {json_file_path}"

    output = ""
    previous_left = 0  # Keep track of the previous left coordinate
    indent_level = 0

    def process_element(element):
        nonlocal output, indent_level, previous_left  # Access outer scope variables
        text_items = element['texts']

        for element in text_items:
            current_text = element['text'].strip()
            # Determine indentation level based on left coordinate
            current_left = element['prov'][0]['bbox']['l']
            # Skip empty text items and bullet points that are not nested
            if len(current_text) == 0 or current_text== 'https://www.DionTraining.com' or current_text == 'CompTIA Network+ (N10-009) (Study Notes)' or current_left > 500:
                continue

            # Determine indentation level based on left coordinate
            if current_left > previous_left:
                indent_level += 1   # Increase indent for nested items
            elif current_left < previous_left:
                indent_level -= 1 # Decrease indent, but not below 0

            indentation = " " * (indent_level * indent_size)
            output += f"{indentation}{current_text}\n"
            previous_left = current_left

    process_element(data)  # Start processing the root of the document
    return output



# Example Usage:
file_path = "/home/chris/Documents/Udemy/CompTIA-Network/studyguide1-50.json"  # Replace with your file path
indented_text = extract_and_indent(file_path)

if "Error" in indented_text:
    print(indented_text)  # Print the error message
else:
    print(indented_text)


# Optionally save the output to a file
def saveToFile(file_path, indented_text):
    try:
        with open(file_path, "w", encoding="utf-8") as outfile:
            outfile.write(indented_text)
    except:
        print("Error saving file.")