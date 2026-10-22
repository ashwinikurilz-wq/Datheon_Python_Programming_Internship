
import random
import os

def load_words():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "words.txt"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        words = [
            line.strip().lower()
            for line in file
            if line.strip().isalpha() and len(line.strip()) >= 4
        ]

    if not words:
        raise ValueError("words.txt does not contain any valid words.")

    return words



HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    ========
    """
]


def display_word(secret_word, guessed_letters):
    """Show guessed letters and hide the remaining letters."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_hangman():
    words = load_words()
    secret_word = random.choice(words)


    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6

    print("\n===== HANGMAN WORD GUESSING GAME =====")
    print("Guess the hidden word one letter at a time!")
    print(f"You have {max_attempts} incorrect guesses available.")

    while wrong_guesses < max_attempts:
        print(HANGMAN_STAGES[wrong_guesses])
        print("Word:", display_word(secret_word, guessed_letters))
        print("Guessed letters:",
              ", ".join(sorted(guessed_letters)) or "None")
        print(f"Incorrect guesses: {wrong_guesses}/{max_attempts}")

        guess = input("\nEnter one letter: ").strip().lower()


        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input! Please enter one letter only.")
            continue


        if guess in guessed_letters:
            print("You already guessed that letter. Try another!")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
        else:
            wrong_guesses += 1
            print("Wrong guess!")


        if all(letter in guessed_letters for letter in secret_word):
            print("\n" + display_word(secret_word, guessed_letters))
            print("Congratulations! You guessed the word!")
            print("YOU WIN!")
            return


    print(HANGMAN_STAGES[wrong_guesses])
    print("The word was:", secret_word.upper())
    print("GAME OVER! You have used all 6 incorrect guesses.")


if __name__ == "__main__":
    play_hangman()
