import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType

model_id = "microsoft/phi-2"

# Load tokenizer and base model in float16 (not 8-bit!)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load and tokenize the articles
dataset = load_dataset("json", data_files="../data/articles.jsonl")

def tokenize(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])

# Setup LoRA config
lora_config = LoraConfig(
    r=8,  # Rank of the LoRA decomposition (controls adapter size). Smaller = more efficient, less expressive.
    lora_alpha=16,  # Scaling factor for the LoRA output. Final scaling = alpha / r = 2. Controls how strong the LoRA update is.
    target_modules=["q_proj", "v_proj"],  # Specifies which layers in the transformer to inject LoRA into.
                                           # Here: query and value projection layers in attention mechanism.
    lora_dropout=0.1,  # Dropout applied to the LoRA layers during training. Helps prevent overfitting (esp. on smaller datasets).
    bias="none",  # Do not train the original model's bias terms. Only train the LoRA adapter weights.
    task_type=TaskType.CAUSAL_LM  # Indicates the model type: Causal Language Model (e.g., GPT, Phi-2).
)


model = get_peft_model(model, lora_config)

# Training arguments
training_args = TrainingArguments(
    output_dir="../model/phi2-financial",  # Directory to save model checkpoints and logs
    num_train_epochs=3,  # Number of times the model will iterate over the entire training dataset
    per_device_train_batch_size=1,  # Batch size per device (GPU/CPU). Low value if you're limited on VRAM.
    learning_rate=2e-4,  # Learning rate for the optimizer. 2e-4 is good for LoRA fine-tuning.
    logging_steps=10,  # Log loss and metrics every 10 training steps (good for monitoring progress)
    save_strategy="epoch",  # Save model checkpoint at the end of each training epoch
    evaluation_strategy="no",  # No evaluation during training (you can change to "steps" or "epoch" if you have a validation set)
    fp16=True,  # Use 16-bit floating point precision (mixed precision) to speed up training and reduce memory use
)


trainer = Trainer(
    model=model,  # The PEFT-wrapped (LoRA) Phi-2 model you're fine-tuning
    args=training_args,  # TrainingArguments you defined earlier (e.g., epochs, batch size, etc.)
    train_dataset=tokenized_dataset["train"],  # The tokenized training dataset (from HuggingFace Datasets)
    tokenizer=tokenizer,  # The tokenizer used to preprocess text; needed for correct padding and decoding
    data_collator=DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal Language Modeling (predict next token), not Masked LM (like BERT)
    )
)


# trainer.train()

# # Save model
# model = model.merge_and_unload()
# model.save_pretrained("../model/phi2-financial")
# tokenizer.save_pretrained("../model/phi2-financial")


# Start the training process
trainer.train()
# Merge the LoRA adapter weights into the base model and unload the adapter
# This results in a single standard model you can use for inference without PEFT
model = model.merge_and_unload()
# Save the merged model to a local directory
model.save_pretrained("../model/phi2-financial")
# Save the tokenizer used for training (so you can tokenize inputs the same way during inference)
tokenizer.save_pretrained("../model/phi2-financial")