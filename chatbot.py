
import json
import re

def load_faq():
    try:
        with open("sample_faq.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: sample_faq.json was not found.")
        return {"greetings": [], "faqs": []}
    except json.JSONDecodeError:
        print("Error: The JSON file has invalid formatting.")
        return {"greetings": [], "faqs": []}


def get_response(message, data):
    message = message.strip().lower()

    if not message:
        return "Please type a question."

    # Exit commands
    if re.fullmatch(r"(bye|exit|quit)", message):
        return "Goodbye!"

    # Greeting detection using the uploaded dataset
    for greeting in data.get("greetings", []):
        if re.search(r"\b" + re.escape(greeting.lower()) + r"\b", message):
            return "Hello! Welcome to the internship support chatbot."

    # Match questions and keywords from the uploaded FAQs
    for faq in data.get("faqs", []):
        question = faq.get("question", "")
        answer = faq.get("answer", "")

        # Match important words from the FAQ question
        keywords = re.findall(r"\b[a-zA-Z0-9]+\b", question.lower())
        keywords = [
            word for word in keywords
            if word not in {
                "what", "are", "the", "how", "do", "i",
                "my", "your", "when", "will", "a", "is",
                "of", "to", "from", "after"
            }
        ]

        if any(
            re.search(r"\b" + re.escape(word) + r"\b", message)
            for word in keywords
        ):
            return answer

    return (
        "Sorry, I didn't understand your question. "
        "You can ask about business hours, project submission, "
        "or your certificate."
    )


def main():
    data = load_faq()

    print("=" * 45)
    print(" INTERNSHIP SUPPORT CHATBOT")
    print("=" * 45)
    print("Ask about business hours, project submission,")
    print("or certificates. Type 'bye' to exit.")

    while True:
        try:
            message = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        response = get_response(message, data)
        print("Bot:", response)

        if re.fullmatch(r"(bye|exit|quit)", message.strip(), re.IGNORECASE):
            break


if __name__ == "__main__":
    main()
