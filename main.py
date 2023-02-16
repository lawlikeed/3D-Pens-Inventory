import tkinter as tk
from tkinter import END
from tkinter import scrolledtext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pen(Base):
    __tablename__ = 'pens'
    serialNo = Column(String, primary_key=True)
    date = Column(String)    
    condition = Column(String)
    notes =Column(String)

    def __init__(self, serialNo, date, condition, notes):
        self.serialNo = serialNo
        self.date = date
        self.condition = condition
        self.notes = notes

    def __repr__(self):
        return f'* ({self.serialNo} {self.date} {self.condition} {self.notes})\n'
    

# Submit pen info to database
def submit_pen():
    date = date_entry.get()
    serialNo = serialNo_entry.get()
    condition = condition_entry.get()
    notes = notes_entry.get("1.0", 'end-1c')
    if len(notes) == 0:
        notes = 'No notes'

    new_pen = Pen(date=date, serialNo=serialNo, condition=condition, notes=notes)
    session.add(new_pen)
    session.commit()

# Find pens from database
def find_pens():
    date = date_entry.get()
    serialNo = serialNo_entry.get()
    condition = condition_entry.get()

    # Get all pens w specified date and save result
    if len(date) == 0:
        pass
    else:
        # print('You made it in dates')
        # print(f'date: {date}')
        # print(f'search_dates: {search_dates(date)}')
        pens_w_dates = search_dates(date)
        print(f'Found pens:\n{pens_w_dates}')
        results_textbox.config(state='normal')
        results_textbox.delete('1.0', END)
        results_textbox.insert(tk.INSERT, str(pens_w_dates))
        results_textbox.config(state='disabled')
    
    # Get all pens w specified SerialNo and save result
    if len(serialNo) == 0:
        pass
    else:
        #print('You made it in serialNo')
        #print(len(serialNo))
        pens_w_serialNo = search_serialNo(serialNo)
        print(f'Found pens:\n{pens_w_serialNo}')
        results_textbox.config(state='normal')
        results_textbox.delete('1.0', END)
        results_textbox.insert(tk.INSERT, str(pens_w_serialNo))
        results_textbox.config(state='disabled')        
    
    # Get all pens w specified condition and save result
    if len(condition) == 0:
        pass
    else:
        pens_w_condition = search_condition(condition)
        print(f'Found pens: {pens_w_condition}\n')
        results_textbox.config(state='normal')
        results_textbox.delete('1.0', END)
        results_textbox.insert(tk.INSERT, str(pens_w_condition))
        results_textbox.config(state='disabled')

# Clean the string of data to remove , and {}'s
def clean_results(data):
    results = str(data)
    results = results[1:-1]
    results = results.replace(', ', '\n')
    return results

# Return 1 pen with the matching serial #
def search_serialNo(SN):
    results = session.query(Pen).filter_by(serialNo=SN).first()
    #print(f'Here is the data:\n{results}')
    return results

# Return all pens with the specified date    
def search_dates(find_date):
    results = session.query(Pen).filter_by(date=find_date).all()
    #print(f'Here is the data before calling the clean_results function:\n{results}')
    results = clean_results(results)
    #print(f'Here is the data after calling the clean_results function:\n{results}')
    return results

# Return all pens with the specified condition
def search_condition(find_condition):
    results = session.query(Pen).filter_by(condition=find_condition).all()
    print(f'Here is the data before calling the clean_results function:\n{results}')
    results = clean_results(results)
    print(f'Here is the data after calling the clean_results function:\n{results}')
    return results









# Initializing database 
engine = create_engine('sqlite:///pens.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Creating GUI
root = tk.Tk()
root.title("3Doodler Pens")
root.geometry("650x330")
root.resizable(False, False)

# Row for padding at top 
header = tk.Label(root, text='')
header.grid(row=0)

# Date 
date_label = tk.Label(root, text="Date")
date_label.grid(row=1, column=0, padx=15, sticky="w")
date_entry = tk.Entry(root)
date_entry.grid(row=1, column=1, sticky="w")

# Serial#
serialNo_label = tk.Label(root, text="Serial #")
serialNo_label.grid(row=2, column=0, padx=15, sticky="w")
serialNo_entry = tk.Entry(root)
serialNo_entry.grid(row=2, column=1, sticky="w")

# Condition
condition_label = tk.Label(root, text="Condition")
condition_label.grid(row=3, column=0, padx=15, sticky="w")
condition_entry = tk.Entry(root)
condition_entry.grid(row=3, column=1, sticky="w")

# Notes
note_label = tk.Label(root, text='Notes')
note_label.grid(row=4, column=0, padx=15, sticky='w')
notes_entry = scrolledtext.ScrolledText(root, width=30, height=7, wrap=tk.WORD)
notes_entry.grid(row=5, column=0, columnspan=2, padx=15)

# Button for submitting info to database
submit_button = tk.Button(root, text="Submit", command=submit_pen)
submit_button.grid(row=6, column=0, padx=15, pady=5, sticky='w')

# Results label
results_label = tk.Label(root, text="Results")
results_label.grid(row=1, column=2, padx=75)

# Cleaning results string from query
temp_output = session.query(Pen).all()
temp_output = clean_results(temp_output)
print(f'\nthis is the temp_output:\n{temp_output}')

# Find button 
find_button = tk.Button(root, text='   Find   ', command=find_pens)
find_button.grid(row=6, column=1, sticky='e', padx=30)

# Results outputted on to GUI
results_textbox = tk.Text(root, height=15, width=40, wrap="word")
results_textbox.grid(row=2, column=2, rowspan=4)
#results_textbox.insert(tk.INSERT, str(temp_output))
results_textbox.config(state='disabled')

# Testing query functions
search_dates('2/14/23')
search_serialNo('123')
search_condition('broke')


root.mainloop()
