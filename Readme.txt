Upload the file
Skip first 7 rows in csv file
Select usefull columns usecols=['Occurred On (NT)', 'Cleared On (NT)', 'MO Name', 'Name']
Remove "NodeB Name=" & after the , part from "MO Name" column
Extract last 2 characters from MO Name column place it as seperate column name ['Region ID']
Extract first 6 characters from MO Name column place it as seperate column name ['Site ID']
Check If 'NOA' tag is include in 'MO Name' then set 'Region ID' to 'NOA'
Move 'Site ID' column to before 'MO Name' column
Add 'Site Type' column to table and define sites as their type
Add 'Duration' column and calculate the Duration
Round up the duration first decimal point
Convert the dataframe to an html table
render the table in the table.html template

#Generate chart
    count the occurrences by site ID
    create a dictionary containing the data for the chart
    print the JSON string to the console in debug mode



