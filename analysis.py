"""
This is a python file that uses the sqlite module to perform sql commands.
The purpose of this program is to find which dinosaurs can be placed
safely together in habitats based on each dinosaur's characteristics.

Herbavores, carnivores, and flying dinosaurs must be kept seprate. Territorial
creatures cannot be placed in the same habitat as other territorial creatures.
Passive creatures can live peacefully with territorial dinosaurs, so the 
passive dinosaurs will be split evenly into the habitats. There are 3 herbavore
habitats, 2 carnivore habitats, and 2 flying habitats.

Info on the dinosaurs was read in form a csv file and placed in a table
in a relational database. Then the database will have a habitat column added.
The databse will be sorted through dino by dino and their habitat key will be
added to the database. Then each habitat will have the dino names printed.
"""
import sqlite3
import csv

# Connect to the database and create a cursor
conn = sqlite3.connect("dino info.db")
curr = conn.cursor()

# Create a table in the databse
createTableCommand = """ CREATE TABLE DINO_DATA (
    Dinosaurname VARCHAR(20),
    Diet VARCHAR(10),
    Territorrial VARCHAR(15),
    Land VARCHAR(10)
);"""
curr.execute(createTableCommand)

# Read the csv file and add the data into the database
with open("Dino Info.csv", 'r') as file:
    i = 0
    for item in file:
        if i > 0:
            stripped_string = item.strip()
            info = stripped_string.split(",")
            addData = f"INSERT INTO DINO_DATA VALUES('{info[0]}','{info[1]}','{info[2]}','{info[3]}')"
            curr.execute(addData)
        else:
            # Skip the first row of the csv file because it contains column titles
            i += 1
            pass

# Add a column to the database to hold the habitat key
addColumn = """ALTER TABLE DINO_DATA
    ADD Habitat VARCHAR(5)"""

curr.execute(addColumn)

# Habitat placement initializers
herbivore_territorial_counter = 1
carnivore_territorial_counter = 1
flying_territorial_counter = 1
next_herbivore_habitat = 1
next_carnivore_habitat = 1
next_flying_habitat = 1

# Grab all the data from the database
fetchData = "SELECT * from DINO_DATA"
curr.execute(fetchData)
answer = curr.fetchall()

# Go through each dino and attach a habitat key
for data in answer:
    habitat = ''

    # Herbavores must be separated
    if data[1] == 'Herbivore':
        habitat += 'H'

        # Only one territorial dino can be placed in a habitat
        # This rotates the terratorial dinos through the habitats
        if data[2] == 'Territorial':
            habitat += str(herbivore_territorial_counter)
            herbivore_territorial_counter += 1

        # Spread the harbavores accross the habitats
        else:
            habitat += str(next_herbivore_habitat)
            next_herbivore_habitat += 1
            # Once a dino is placed in the last habitat, cycle back to the first
            if next_herbivore_habitat == 4:
                next_herbivore_habitat = 1

    # Flying Dinosaurs must be kept together
    elif data[3] == 'Flying':
        habitat += 'F'
        # One territorial dino per habitat
        if data[2] == 'Territorial':
            habitat += str(flying_territorial_counter)
            flying_territorial_counter += 1

        # Spread the non-territorial dinosaurs across the habitats
        else:
            habitat += str(next_flying_habitat)
            next_flying_habitat += 1
            # Once a dino is placed in the last habitat, cycle back to the first
            if next_flying_habitat == 3:
                next_flying_habitat = 1
            
    # Carnivores must be placed together
    elif data[1] == 'Carnivore':
        habitat += 'C'
        # One territorial dino per habitat
        if data[2] == 'Territorial':
            habitat += str(carnivore_territorial_counter)
            carnivore_territorial_counter += 1

        # Non-territorial dinos are spread accross the habitats
        else:
            habitat += str(next_carnivore_habitat)
            next_carnivore_habitat += 1
            # Once a dino is placed in the last habitat, cycle back to the first
            if next_carnivore_habitat == 3:
                next_carnivore_habitat = 1
               

    # Add the dinosaur's habitat key to the database 
    name = data[0]
    update = f"""UPDATE DINO_DATA
        SET Habitat = '{habitat}'
        WHERE Dinosaurname = '{name}'
        """
    curr.execute(update)

# Save all changes made to the database
conn.commit()

# Get all dinosaurs in the database and sort them by habitat
fetchData = """SELECT Dinosaurname, Habitat
    FROM DINO_DATA
    ORDER BY Habitat"""

curr.execute(fetchData)
answer = curr.fetchall()

# Report the findings
for data in answer:
    print(f"The {data[0]} goes into habitat {data[1]}")

