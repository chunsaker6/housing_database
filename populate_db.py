import csv
import subprocess

def main():
    # Open the CSV file in read mode
    with open('Housing.csv', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Iterate over each row in the CSV file
        for row in reader:
            # print(row[0])
            # Bash command to execute
            bash_command = "ls -l"
            bash_command = "./face adduser $i\"@gmail.com\""
            # # Execute the Bash command
            result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)

main()