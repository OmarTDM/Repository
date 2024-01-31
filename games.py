from pdb import run
import random 

def play_game():
    options = ("rock", "paper", "scissors")
    player = None
    computer = random.choice(options)

    while True:
        while player not in options:
            player = input("Enter a choice (rock, paper, scissors): ")

        print(f"Player: {player}")
        print(f"Computer: {computer}")

        if player == computer:
            print("It's a tie!")

        elif player == "rock" and computer == "scissors":
            print("You win!")

        elif player == "paper" and computer == "rock":
            print("You win!")

        elif player == "scissors" and computer == "paper":
            print("You win!")

        else: 
            print("You lose!")

while True:
    play_game()
    new_game = input("Do you want to start a new game? (y/n): ").lower()
    if new_game != "y":
