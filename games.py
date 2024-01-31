import random

def get_user_choice():
    user_choice = input("Kies steen, papier of schaar: ").strip().lower()
    while user_choice not in ['steen', 'papier', 'schaar']:
        print("Ongeldige keuze. Kies opnieuw: steen, papier of schaar.")
        user_choice = input("Kies steen, papier of schaar: ").strip().lower()
    return user_choice

def get_computer_choice():
    return random.choice(['steen', 'papier', 'schaar'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Gelijkspel!"
    elif (user_choice == 'steen' and computer_choice == 'schaar') or \
         (user_choice == 'papier' and computer_choice == 'steen') or \
         (user_choice == 'schaar' and computer_choice == 'papier'):
        return "Je wint!"
    else:
        return "Computer wint!"

def main():
    print("Welkom bij Steen, Papier, Schaar!")

    while True:
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()

        print(f"Jij koos {user_choice}.")
        print(f"Computer koos {computer_choice}.")

        result = determine_winner(user_choice, computer_choice)
        print(result)

        play_again = input("Wil je nog een keer spelen? (ja/nee): ").strip().lower()
        if play_again != 'ja':
            break

    print("Bedankt voor het spelen!")

if __name__ == "__main__":
    main()
