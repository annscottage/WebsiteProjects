# First of all we import the methods that we will need to do this work
import pandas as pd
# import requests
import sys

# Now we import the Excel spreadsheet/worksheet that holds all of the data 
books = pd.read_excel(r'C:\Users\IlluminateBookshop\OneDrive - Illuminate Trust Ltd\SHB\SHB  Edited for Website.xlsx', sheet_name = 'Sheet1')

# Start by dropping the columns that were pulled in that are not required
columns_to_drop = ['Column1'] # These are the columns we don't want
books = books.drop(columns_to_drop, axis=1) # Here we drop those columns listed above

#Now we want to change the column names so that there are no problematic characters in them
books.columns = books.columns.str.replace("(", "").str.replace(")","")

# Now we format all column headings so that they are in 'title' format
books.columns = books.columns.str.title()
# Except for 'ISBN' which can be in capitals
books.rename({"Isbn": "ISBN"}, axis=1, inplace=True)

# And now we do the same formatting to all of the entries in the columns, so that they are easier to read on the website
books['Title'] = books['Title'].str.title().str.replace(r"'S", "'s")
books['Authors'] = books['Authors'].str.title()
books['Category'] = books['Category'].str.title()
books['Binding'] = books['Binding'].str.title()
books['Condition'] = books['Condition'].str.title()
books['Notes'] = books['Notes'].str.title()

# We want to get rid of any £ signs in price and also format it as a number to two decimal places
books.Price = books.Price.astype(str)
books.Price = books.Price.str.replace("£", "").str.replace("p","").str.replace("P", "")
books.Price = books.Price.astype(float, '%.2f', errors = 'ignore')

# Before we save the file, we want to check that all of the entries in the 'Book No' column are unique

CheckBooks = books.iloc[:,[0,1,7]]

duplicateBookNos = CheckBooks[CheckBooks.duplicated(['Book No'], keep = False)]
if len(duplicateBookNos) == 0:
    print()
    print('There are no duplicate Book Nos in this file')
    print()
    
if len(duplicateBookNos) != 0:
    print()
    print("This is a list of any entries with duplicated Book Nos:")
    print()
    print (duplicateBookNos, sep='\n')
    print()
    print("Please make a note of the numbers/titles/categories, remove the duplicate numbers from the Excel spreadsheet and run this programme again.")
    print()
    text = input("Please press ENTER to terminate this programme")
    sys.exit()

# For the new website format we need to remove the 'http://' part of the Google Search address because this doesn't work on a website.
books['Google Book Search'] = books['Google Book Search'].str.replace(r'http://','')
    
# And finally export it to the right folder with the right name for Importing into the Website
sample = books.iloc[:,0:11]
sample.ISBN = sample.ISBN.astype(str) + " "
sample.to_csv(r'C:\Users\IlluminateBookshop\OneDrive - Illuminate Trust Ltd\SHB\2ndHBImport.csv', index = False)

# Use FTP process to upload to the website folders
import subprocess
subprocess.call([r'C:\Users\IlluminateBookshop\OneDrive - Illuminate Trust Ltd\SHB\WebsiteUpload.bat'])

print('The data conversion was SUCCESSFUL and the results have been uploaded to the website')
print()
text = input("Please press ENTER to terminate this programme")
sys.exit()


