import csv
import subprocess

def main():
    # Open the CSV file in read mode
    with open('Housing.csv', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        subprocess.run('./housing.py create', shell=True)
        # Iterate over each row in the CSV file
        #count = 0
        for i, row in enumerate(reader):
            if i != 0:
                #print(row[0])
                # Bash command to execute
                #addBasics
                price = row[2]
                bedroom = row[3]
                bathroom = row[4]
                command_bash = './housing.py addbasics ' + price + ' ' + bathroom + ' ' + bedroom 
                # # Execute the Bash command
                result = subprocess.run(command_bash, shell=True, capture_output=True, text=True)
                #print(result.stdout)
        
                #addTime
                property_listing = row[1]
                year_built = row[14]
                year_reno = row[15]
                command_time = './housing.py addtime ' + property_listing + ' ' + year_built + ' ' + year_reno 
                result = subprocess.run(command_time, shell=True, capture_output=True, text=True)
                #print(result.stdout)

                #addAmenities
                floors = row[7]
                waterfront = row[8]
                view = row[9]
                condition = row[10]
                grade = row[11]

                command_amenities = './housing.py addamenities ' + floors + ' ' + waterfront + ' ' + view + ' ' + condition + ' ' + grade
                result = subprocess.run(command_amenities, shell=True, capture_output=True, text=True)
                #print(result.stdout)


                #addLocation
                zipcode = row[16]
                lat = row[17]
                longitude = row[18]

                command_loc = './housing.py addlocation -- ' + zipcode + ' ' + lat + ' ' + longitude
                result = subprocess.run(command_loc, shell=True, capture_output=True, text=True)
                #print(result.stdout)

                #addSqft
                live = row[5]
                lot = row[6]
                above = row[12]
                basement = row[13]

                command_sqft = './housing.py addsqft ' + live + ' ' + lot + ' ' + above + ' ' + basement
                result = subprocess.run(command_sqft, shell=True, capture_output=True, text=True)
                #print(result.stdout)

                #count+=1
main()
