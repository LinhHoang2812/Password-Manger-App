from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list.extend([random.choice(symbols) for char in range(nr_symbols)])
    password_list.extend([random.choice(numbers) for char in range(nr_numbers)])

    random.shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #   password += char

    password_entry.delete(0,END)
    password_entry.insert(0,password)
    pyperclip.copy(password)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_dict ={
        website: {
            "Email": email,
            "Password": password
        }
    }

    if len(website)==0 or len(email)==0 or len(password) == 0 :
        messagebox.showinfo(title="Oops",message="Please dont leave any fields empty")
    else:


        is_ok = messagebox.askokcancel(title=website, message=f"These are the info entered:\nEmail:{email}\n"
                                                              f"Password: {password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("password.json","r") as password_data:
                    #open json file as dictionary
                    data= json.load(password_data)
            except FileNotFoundError:
                with open("password.json","w") as password_data:
                    #dump the first data ever inserted into the json file to create a new json file
                    json.dump(new_dict, password_data, indent=4)
            else:
                # update the dictionary with new data
                data.update(new_dict)
                with open("password.json", "w") as password_data:
                    # dump the updated data into the json file
                    json.dump(data, password_data, indent=4)
            finally:
                    website_entry.delete(0,END)
                    password_entry.delete(0,END)

#-----------------------------SEARCH PASSWORD --------------------------------------- #

def search():
    website = website_entry.get()

    try:
        with open("password.json","r") as password_file:
            data = json.load(password_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No data found.")
    else:
        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No detail for {website} exists.")






# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Password Manager")
window.config(padx=50,pady=50)

clocker_image= PhotoImage(file='logo.png')
canvas = Canvas(width=200,height=200)
canvas.create_image(100,100,image=clocker_image)
canvas.grid(column=1,row=0)

website_label = Label(text="Website")
website_label.grid(column=0,row=1)

website_entry = Entry(width=19)
website_entry.grid(column=1,row=1)
website_entry.focus()


email_label = Label(text="Email/Username")
email_label.grid(column=0,row=2)

email_entry= Entry(width=35)
email_entry.grid(column=1,row=2,columnspan=2)
email_entry.insert(END,"abc@gmail.com")

password_label = Label(text="Password")
password_label.grid(column=0,row=3)

password_entry= Entry(width=19)
password_entry.grid(column=1,row=3)


pass_gen_button = Button(text="Generate Password",width=11,command=password_gen)
pass_gen_button.grid(column=2,row=3)

add_button = Button(text="Add",width=36,command=save)
add_button.grid(column=1,row=4,columnspan=2)

search_button= Button(text="Search",width=9, command=search)
search_button.grid(column=2, row=1)





window.mainloop()