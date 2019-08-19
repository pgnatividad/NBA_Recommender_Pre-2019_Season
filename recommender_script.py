import pandas as pd
master_df = pd.read_csv("data/master_recommender.csv")
import time
from PIL import Image #for easter egg

#did this just to make sure I dont overwrite the master
copy_recommender = master_df.copy()
copy_recommender.index=copy_recommender.columns

#this df is mostly used for the search
career_df=pd.read_csv("data/total_career_stats_of_players_df.csv")
header = ['Name','Score (Lower is Better)']
removed_players = []


print('\n\n\n')
#Here is the function for the main menu
def main_menu():

    print('''
    Welcome to the Recommender
    Type 1 to search of recommended players
    Type 2 to remove available players
    Type 3 to add a player back into the pool
    Type 4 to view the unavailable players
    Type 6 to learn about caveats
    Type 9 to exit
    ''')
    entry = input('What is your input \n > ')

    if entry == '1':
        search()
    elif entry == '2':
        remove()
    elif entry =='3':
        add()
    elif entry == '9':
        exit()
    elif entry =='4':
        print_removed()
    elif entry == '6':
        print('''
        This Recommender only works for players who are on teams
        for the 2019-2020 season prior mid-July 2019
        ''')
        main_menu()
    else:
        print('please put a valid choice')
        time.sleep(1) #makes the user wait before getting prompted the main menu
        main_menu()



def search(): #the function that takes a player and returns their 10 more similar available players

    print('''
    This is the search function
    Enter Your Player of interest
    Note: Type the name as it appears in Basketball Reference
    Note: Type the first 3 characters of their name to help see
    how the name should be typed out ''')
    query = input('Type 9 to exit \n>')
    if query == '9':
        main_menu()

    elif query == 'jingles': #Easter Egg
        print(header)
        print(copy_recommender['Joe Ingles'].sort_values()[0:11])
        Image.open("jingled.png").show()



#real searches now
    elif career_df.loc[career_df['name'].str.contains(query),'name'].shape[0] == 0: #means the name isnt found in recommender
        print("try spelling their name exactly from Basketball Ref")


    elif career_df.loc[career_df['name'].str.contains(query),'name'].shape[0] ==1: #either the user spelled the full name correctly or just received one result on their search

        try: #spelled name correctly
            print(header)
            print(copy_recommender[query].drop(removed_players).sort_values()[0:11])
        except: #just one result on their search
            print("did you mean: ")
            print(career_df.loc[career_df['name'].str.contains(query),'name'])


    elif career_df.loc[career_df['name'].str.contains(query),'name'].shape[0] >1: #can't use recommender if they specify more than 1 person
        print("did you mean: ")
        print(career_df.loc[career_df['name'].str.contains(query),'name'])


    else:
        print('please put a valid choice')
        time.sleep(1)
        search()



    continue_indicator =input('Continue searching? 1 for yes,2 for no\n > ')
    if continue_indicator == '1':
        search()
    elif continue_indicator =='2':
        main_menu()
    else:
        print("I'm going to assume you meant 2")
        time.sleep(1)
        main_menu()

def remove(): #this function removes players from the available player pool

    print('''
    This is the remove function
    Enter the player you want to remove
    Type 9 to exit
    Type 1 to view the removed players

    ''')
    removal_input = input(' > ')
    if removal_input == '9':
        main_menu()
    elif removal_input == '1':
        print(removed_players)
    elif career_df.loc[career_df['name'].str.contains(removal_input),'name'].shape[0] ==0:
        print("try spelling their name exactly from Basketball Ref")
    elif career_df.loc[career_df['name'].str.contains(removal_input),'name'].shape[0] ==1:
        try: #spelled name correctly
           copy_recommender[removal_input].sort_values()[0:2] #this is to force the error
           #if i did not force the error the except will never catch
           #this makes sure the person does not oput half a name and it gets added to the list
           removed_players.append(removal_input)
           print(f'{removal_input} has been removed')

        except: #just one result on their search
            print("did you mean: ")
            print(career_df.loc[career_df['name'].str.contains(removal_input),'name'])
    elif career_df.loc[career_df['name'].str.contains(removal_input),'name'].shape[0] >1:
        print("did you mean: ")
        print(career_df.loc[career_df['name'].str.contains(removal_input),'name'])

    else:
        print('please put a valid choice')
        time.sleep(1)
        remove()


    continue_indicator_2 = input('Continue removing? 1 for yes,2 for no\n > ')
    if continue_indicator_2 == '1':
        remove()
    elif continue_indicator_2 == '2':
        main_menu()
    else:
        print("I'm gonna assume you meant 2")
        time.sleep(1)
        main_menu()

def add(): #this function adds players back to the player pool
    print('''
    To add a person back
    type in their name
    type 1 to see the removed player list
    type 9 to exit
    ''')
    add_input = input(">")

    if add_input == '9':
        main_menu()
    elif add_input == '1':
        print(removed_players)
    elif add_input not in removed_players:
        print(f"{add_input} is not in the removed players list")
    elif add_input in removed_players:
        removed_players.remove(add_input)
        print(f'{add_input} has been added back into the available players pool')
    else: #error catch that should never happen
        print('im not sure what caused this')

    continue_indicator_3 = input('Continue Adding? 1 for yes, 2 for no \n>')
    if continue_indicator_3 =='1':
        add()
    elif continue_indicator_3 =='2':
        main_menu()
    else:
        print("I'm gonna assume you meant 2")
        time.sleep(1)
        main_menu()

def print_removed(): #this prints the removed player list
    if len(removed_players)<1:
        print("List is Empty")
    else:
        print(removed_players)
    #time.sleep(1)
    main_menu()

main_menu() #runs the code
