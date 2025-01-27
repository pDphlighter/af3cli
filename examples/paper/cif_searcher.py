def search_in_cif(file_path, search_string):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Search for the string in each line
        matching_lines = [line.strip() for line in lines if search_string in line]

        if matching_lines:
            print(f"Found '{search_string}' in the following lines:")
            for match in matching_lines:
                print(match)
        else:
            print(f"'{search_string}' was not found in the file.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


search_string = "WNT"
cif_file_path = "/home/doepnerp/Projekte/Development/local/python_scripts/python_sandbox/components.cif"

if __name__ == "__main__":
    search_in_cif(cif_file_path, search_string)