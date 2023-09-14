import tkinter as tk
from tkinter import ttk, Text, Scrollbar
from llama_cpp import Llama
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Initialize Llama model
llm = Llama(model_path="C:\\Users\\gray00\\llama-2-7b.ggmlv3.q8_0.bin", n_ctx=3999)
executor = ThreadPoolExecutor(max_workers=1)

# Function to save data to JSON
def save_to_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Function to load data from JSON
def load_from_json(filename='courses.json'):
    with open(filename, 'r') as f:
        return json.load(f)

# Function to generate response from Llama
async def llama_generate_async(prompt):
    loop = asyncio.get_event_loop()
    output = await loop.run_in_executor(executor, lambda: llm(prompt, max_tokens=1999))
    return output

# Function to handle course selection and generate content using Llama
async def handle_course_selection(event):
    selected_index = event.widget.curselection()[0]
    selected_course = app.courses['courses'][selected_index]
    prompt = f"You are Dave a Humoid Model Working with HUmans to Generate content for the educational courses professionaly. Please do anything very excellent For the Course {selected_course['title']}"
    generated_content = await llama_generate_async(prompt)
    app.course_content.delete(1.0, tk.END)
    app.course_content.insert(tk.END, generated_content)

# Main App Class
class HumanityHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HumanityHub by Gray00")
        self.geometry("800x600")
        self.courses = load_from_json()
        self.init_UI()

    def init_UI(self):
        # Create Tabs
        tab_control = ttk.Notebook(self)
        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)
        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Education')
        tab_control.add(tab2, text='Entertainment')
        tab_control.add(tab3, text='Cooperation')
        tab_control.pack(expand=1, fill='both')

        # Education Tab
        lbl1 = tk.Label(tab1, text="Educational Courses")
        lbl1.pack()
        self.course_listbox = tk.Listbox(tab1)
        scrollbar = Scrollbar(tab1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.course_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.course_listbox.yview)
        for course in self.courses['courses']:
            self.course_listbox.insert(tk.END, course['title'])
        self.course_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.course_listbox.bind('<<ListboxSelect>>', lambda event: asyncio.run(handle_course_selection(event)))

        self.course_content = Text(tab1, wrap=tk.WORD)
        self.course_content.pack(expand=1, fill=tk.BOTH)

        # Entertainment Tab
        lbl2 = tk.Label(tab2, text="Entertainment Media")
        lbl2.pack()

        # Cooperation Tab
        lbl3 = tk.Label(tab3, text="Collaboration Spaces")
        lbl3.pack()

        # AI Assistant
        self.ai_input = tk.Entry(self, width=50)
        self.ai_input.pack(side=tk.LEFT)
        self.ai_button = tk.Button(self, text="Ask Llama", command=lambda: asyncio.run(self.ask_llama()))
        self.ai_button.pack(side=tk.RIGHT)

    async def ask_llama(self):
        user_input = self.ai_input.get()
        self.ai_input.delete(0, tk.END)
        response = await llama_generate_async(user_input)
        print(f"Llama: {response}")

if __name__ == "__main__":
    app = HumanityHub()
    app.mainloop()
