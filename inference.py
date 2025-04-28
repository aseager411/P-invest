import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Path to your fine-tuned model
model_path = "model/phi2-financial"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32, device_map="cpu")

# Define a function to generate a response
def ask_model(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
if __name__ == "__main__":
    while True:
        question = input("\nAsk a finance question (or type 'quit' to exit):\n> ")
        if question.lower() == "quit":
            break
        response = ask_model(question)
        print("\nModel says:\n", response)
