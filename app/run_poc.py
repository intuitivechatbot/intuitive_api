from app.query_engine import ask_query

def main():
    print("\n🌿 Welcome to the Herbal RAG Assistant 🌿")
    print("Type 'exit' to quit.\n")

    while True:
        query_type = input("Ask about [info] or [symptom]? (type 'info' or 'symptom'): ").strip().lower()
        if query_type not in ["info", "symptom"]:
            print("Please type 'info' or 'symptom'.")
            continue

        user_input = input("\nEnter your question or symptom description: ").strip()
        if user_input.lower() == "exit":
            break

        answer = ask_query(user_input, query_type=query_type)
        print("\n🧠 Answer:\n", answer)
        print("\n"+"-"*50)

if __name__ == "__main__":
    main()