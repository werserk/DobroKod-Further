def load_prompt(filename):
    with open(f"src/prompts/{filename}", "r") as file:
        return file.read()
