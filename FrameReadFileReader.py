import re

class FrameCoordFileReader:
    def __init__(self, file1_path, file2_path):
        self.file1_data = self.load_file(file1_path)
        self.file2_data = self.load_file(file2_path)

    def load_file(self, file_path):
        """Loads SSC file data, returning a list of lines."""
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines

    def find_station_in_file(self, station_name, file_data):
        """Finds all lines for a given station in the file."""
        station_lines = [line for line in file_data if station_name in line]
        return station_lines

    def show_station_info(self, station_name):
        """Displays the first and last six lines of a given station from both files."""
        # Find lines in file 1
        file1_lines = self.find_station_in_file(station_name, self.file1_data)
        # Find lines in file 2
        file2_lines = self.find_station_in_file(station_name, self.file2_data)

        # Display the first and last six lines for file 1
        print(f"\nStation {station_name} in file 1:")
        if file1_lines:
            print("First line:")
            print(file1_lines[0])
            print("Last 6 lines:")
            for line in file1_lines[-6:]:
                print(line)
        else:
            print(f"Station {station_name} not found in file 1.")

        # Display the first and last six lines for file 2
        print(f"\nStation {station_name} in file 2:")
        if file2_lines:
            print("First line:")
            print(file2_lines[0])
            print("Last 6 lines:")
            for line in file2_lines[-6:]:
                print(line)
        else:
            print(f"Station {station_name} not found in file 2.")

    def compare_station(self, station_name):
        """Compares the data for the given station from the last six lines in both files."""
        file1_lines = self.find_station_in_file(station_name, self.file1_data)[-6:]
        file2_lines = self.find_station_in_file(station_name, self.file2_data)[-6:]

        if len(file1_lines) < 6 or len(file2_lines) < 6:
            print(f"\nCannot compare the last six lines for station {station_name}, insufficient data.")
            return

        print(f"\nComparison of the last six lines for station {station_name}:")

        # Helper function to split lines into elements and convert to float where possible
        def parse_line_to_numbers(line):
            # Remove multiple spaces and split the line
            elements = re.split(r'\s+', line.strip())
            # Convert to numbers where possible
            parsed_elements = []
            for el in elements:
                try:
                    parsed_elements.append(float(el))
                except ValueError:
                    parsed_elements.append(el)  # Leave non-numeric elements as they are
            return parsed_elements

        # Iterate over the last six rows
        for i in range(6):
            print(f"\nComparison of line {6 - i}:")
            parsed_file1 = parse_line_to_numbers(file1_lines[i])
            parsed_file2 = parse_line_to_numbers(file2_lines[i])

            # Subtract numeric values in the rows
            differences = []
            for el1, el2 in zip(parsed_file1, parsed_file2):
                if isinstance(el1, float) and isinstance(el2, float):
                    # Format the difference to five decimal places with "m"
                    differences.append(f"{el1 - el2:.5f} m")
                else:
                    differences.append("N/A")  # If not numeric, differences do not apply

            # Display differences
            print(f"File 1: {file1_lines[i]}")
            print(f"File 2: {file2_lines[i]}")
            print("Differences:")
            print(differences)

    def show_comparison(self, station_names):
        """Performs analysis for one or more stations."""
        if isinstance(station_names, str):
            station_names = [station_names]

        for station_name in station_names:
            self.show_station_info(station_name)
            self.compare_station(station_name)


# Example usage
dict_path = r'C:/M_Mikos'
ssc_reader = FrameCoordFileReader(dict_path+'/'+'ITRF2020-IGS-TRF.SSC.txt', dict_path+'/'+'IGS20.ssc.txt')
ssc_reader.show_comparison(['BRUX', 'BOR1'])
