"""
This script is a GUI that inports a CSV file from a ballot, splitting it into
one anonymous file of votes and one file of voter information.

The script allows the user to select a CSV file, processes it to count votes for each candidate.

The input CSV has 2 key columns:

Attendee name - the name of the voter. Each name occurs up to 5 times, and we need to record all unique
names in this column.

Event type - the name of the candidate. Each candidate can have multiple votes, and we need to count the 
total votes for each candidate.

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
        if 'Attendee name' not in df.columns or 'Event type' not in df.columns:
            raise ValueError("CSV file must contain 'Attendee name' and 'Event type' columns.")

        # Count votes for each candidate
        vote_counts = df['Event type'].value_counts()

        # Create a list of unique voters
        unique_voters = df['Attendee name'].unique()
        
        # Remove voters called "Booking fee total" or "Total"
        unique_voters = [voter for voter in unique_voters if voter not in ["Booking fee total", "Total"]]
        
        # Create a DataFrame for the results
        result_df = vote_counts.reset_index()
        result_df.columns = ['Candidate', 'Votes']
        
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