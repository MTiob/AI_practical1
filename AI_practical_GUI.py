#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tkinter import *
from tkinter import ttk
import AI_practical_body as AI


window = Tk()
window.title("AI Practical 1")
window.geometry("640x480")
window.resizable(False, False)
window.grid_rowconfigure(0, weight = 1)
window.grid_columnconfigure(0, weight = 1)

game_start_frame = Frame(window, bg = "azure")
game_start_frame.grid(row = 0, column = 0, sticky = "nsew")
game_play_frame = Frame(window, bg = "azure") 
game_play_frame.grid(row = 0, column = 0, sticky = "nsew")

game_start_frame.tkraise()

window.option_add("*TCombobox*Listbox.font", "Helvetica 14")
    
explanation_text = ("                                                    Game Rule\n"
        "Each player has 32 points and shares a string containing [2,2,2,2,3,3,3,5,5,5,7,7].\n"
        "Each player select 1 number from string every itsown turn.\n" 
        "The player subtracts selected number from own points,\nand remove selected number from the string.\n" 
        "Afterwards player passes turn to opponent.\n"
        "Game continues until string becomes empty.\n"
        "After finishing game, player who has less score wins the game.\n"
        "When your turn, select number from dropbox and press Next step button\n"
        "If computer's turn, just press Next step button to procede")

player = StringVar()
victory = StringVar()
score1 = StringVar()
score2 = StringVar()
string = StringVar()
chosen_num = StringVar()
game_status = StringVar()
turn_player = StringVar()
num_choice = (2,3,5,7)


num_choice_combo = ttk.Combobox(game_play_frame, state="readonly", textvariable = chosen_num, values = num_choice, font = ("Helvetica", "14"))
back_button = Button(game_play_frame, text="Restart game", width=20, font=("Helvetica", "12"), relief = RAISED, command = lambda: [change_frame(game_start_frame, game_play_frame)])
turn_player_label = Label(game_play_frame, textvariable = turn_player, font=("Helvetica", "14"))
turn_player_label["bg"] = "azure"

def set_num_choice(tmp_string):
    global num_choice
    tmp = []
    for i in [2, 3, 5, 7]:
        if i in tmp_string:
            tmp.append(i)
        else:
            continue
    num_choice = tuple(tmp)
    num_choice_combo.configure(value = num_choice)
        
def set_game_status(score1, score2, string):
    game_status.set("Player's score:" + str(score1.get()) + " : " + str(string.get()) + ":" + "Computer's score:" +str(score2.get()))
    
def get_game_result(result):
    tmp = result
    if len(tmp) == 4:
        score1.set(tmp[0])
        score2.set(tmp[1])
        string.set(tmp[2])
        set_turn(tmp[3])
        set_game_status(score1, score2, string)
        set_num_choice(tmp[2])
    else:
        score1.set(tmp[0])
        score2.set(tmp[1])
        string.set([])
        set_turn(tmp[3])
        set_game_status(score1, score2, string)
        victory.set(str(tmp[4]) + " win the game\nIf you want to start new game, press restart game\notherwise, close the window to finish the game")
        turn_player_label.pack_forget()
        back_button.pack(side = BOTTOM, pady = 30)
        
def set_turn(turn_p):
    if turn_p:
        turn_player.set("Player's turn")
    else:
        turn_player.set("Computer's turn")

def change_frame(frame_name, ex_frame_name):
    children = ex_frame_name.winfo_children()
    for child in children:
        child.destroy
    frame_name.tkraise()

def game_start_page():
    
    def get_player():
        player = select_turn_combo.get()
        if player == "Player":
            return True
        else:
            return False
    
    #item declaration for game start page
    player_choice = ["Player", "Computer"]
    select_turn_label = Label(game_start_frame, text="Pick who taking first move", font=("Helvetica", "14"))
    select_turn_label["bg"] = "azure"
    select_turn_combo = ttk.Combobox(game_start_frame, state="readonly", textvariable = player, values = player_choice, font = ("Helvetica", "14"))
    select_turn_combo.set(player_choice[0])
    start_game_button = Button(game_start_frame, text="Start game",  font=("Helvetica", "12"), relief = RAISED, command = lambda: [game_play_page(get_player()), set_turn(get_player()), change_frame(game_play_frame, game_start_frame)])
    game_explanation = Label(game_start_frame, text = explanation_text, font=("Helvetica", "12"), justify="left")
    game_explanation["bg"] = "azure"
    
    #placement of items on game start page
    select_turn_label.pack(side = TOP, pady=20)
    select_turn_combo.pack(side = TOP, pady=10)
    start_game_button.pack(side = TOP, pady=30)
    game_explanation.pack(side = TOP, pady=10)
    
def game_play_page(turn_player1):
    #item declaration for game play page
    game = AI.game_concept(turn_player1)
    
    score1.set(32)
    score2.set(32)
    string.set([2,2,2,2,3,3,3,5,5,5,7,7])
    set_game_status(score1, score2, string)
    
    def selected(event):
        tmp = num_choice_combo.get()
        chosen_num.set(tmp)
        
    
    game_status_label = Label(game_play_frame, textvariable = game_status, font=("Helvetica", "14"))
    game_status_label["bg"] = "azure"  
    victory_label = Label(game_play_frame, textvariable = victory, font=("Helvetica", "14"))
    victory_label["bg"] = "azure"
    num_choice_combo.set(num_choice[0])
    num_choice_combo.bind("<<ComboboxSelected>>", selected)
    next_step_button = Button(game_play_frame, text="Next step",  font=("Helvetica", "12"), relief = RAISED, command = lambda: [get_game_result(game.main(int(chosen_num.get())))])
    
    #placement of items on game play page
    victory_label.pack(side = TOP, pady=20)
    turn_player_label.pack(side = TOP)
    game_status_label.pack(side = TOP, pady=20)
    num_choice_combo.pack(side = TOP, pady=30)
    next_step_button.pack(side = TOP, pady=30)



game_start_page()
window.mainloop()

