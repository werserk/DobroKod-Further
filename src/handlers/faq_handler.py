# Example FAQs, ideally these would be loaded from a file or database
FAQs = {
    "What is cancer?": "Cancer is a disease where cells in the body grow out of control.",
    "How do I contact a doctor?": "You can contact a doctor by sending a message with your query. A doctor will respond shortly."
}


def handle_faq(question):
    return FAQs.get(question, None)
