"""
This script is a GUI that inports a CSV file from a ballot, splitting it into
one anonymous file of votes and one file of voter information.

The script allows the user to select a CSV file, processes it to count votes for each candidate.

The input CSV has one column for the voter name, and one column for each candidate's votes.

Attendee name - the name of the voter. 

Columns 7 to the maximum column are the candidates, with the votes for each candidate in the rows below.
The script counts the votes for each candidate and saves the results in a new CSV file named 'vote_counts.csv'.
The unique voters are saved in a separate CSV file named 'voters.csv'.

The script uses the pandas library to read the CSV file, and tkinter for the GUI interface.
"""
import pandas as pd
from tkinter import Tk, filedialog, messagebox
import os

def count_votes(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Check if required columns are present
        if 'Attendee name' not in df.columns:
            raise ValueError("CSV file must contain 'Attendee name' column.")
        
        # Create a list of unique voters
        unique_voters = df['Attendee name'].unique()
        
        # Remove voters called "Booking fee total" or "Total"
        unique_voters = [voter for voter in unique_voters if voter not in ["Booking fee total", "Total"]]
        
        # Find the names of the candidates, which are all columns 6 onwards
        candidate_columns = df.columns[6:]  # Assuming the first 6 columns are not candidates
        if candidate_columns.empty:
            raise ValueError("No candidate columns found in the CSV file.")
        candidate_columns = candidate_columns.tolist()

        # Count votes for each candidate, by summing the values in each candidate column
        votes = []
        for candidate in candidate_columns: 
            votes += [sum(df[candidate]==1)]
        # Create a new DataFrame with the candidate names and their corresponding vote counts
        result_df = pd.DataFrame({
            'Candidate': candidate_columns,
            'Votes': votes
        })
        # Sort the DataFrame by the number of votes in descending order
        result_df = result_df.sort_values(by='Votes', ascending=False).reset_index(drop=True)
                
        # Now that we've extracted the voters, delete the input file.
        os.remove(file_path)

        return result_df, unique_voters

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None
    
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        result_df, unique_voters = count_votes(file_path)
        if unique_voters is not None:
            result_df.to_csv('vote_counts.csv', index=False)
            # Unique_votes is list, so we convert it to a DataFrame
            unique_voters_df = pd.DataFrame(unique_voters, columns=['Attendee name'])
            # Save unique voters to a CSV file
            unique_voters_df.to_csv('voters.csv', index=False)
            messagebox.showinfo("Success", "Input file deleted\n Vote counts saved to 'vote_counts.csv'\n Voters saved to 'voters.csv'.",
                                icon='info')
            # Display the first up to 10 rows of the vote counts in a message box
            messagebox.showinfo("Vote Counts", result_df.head(10).to_string(index=False), 
                                icon='info')
            
            
def main():
    root = Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Info", "Select a CSV file to count votes.", icon='info')
    select_file()
    root.destroy()
    
if __name__ == "__main__":
    main()