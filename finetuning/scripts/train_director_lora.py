from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model

# =========================
# CONFIG
# =========================
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATA_PATH = "../data/director.jsonl"
OUTPUT_DIR = "../adapters/director_lora"
MAX_LENGTH = 512

# =========================
# LOAD MODEL & TOKENIZER
# =========================
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

# =========================
# APPLY LoRA
# =========================
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)

# =========================
# TOKENIZATION FUNCTION
# =========================
def tokenize_fn(example):
    prompt = example["instruction"]
    response = example["output"]

    full_text = prompt + "\n" + response

    tokens = tokenizer(
        full_text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
    )

    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

# =========================
# LOAD & PROCESS DATASET
# =========================
dataset = load_dataset("json", data_files=DATA_PATH)

dataset = dataset.map(
    tokenize_fn,
    remove_columns=dataset["train"].column_names,
)

# =========================
# TRAINING ARGS (MAC SAFE)
# =========================
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=False,  # ❌ NO fp16 on Mac
    logging_steps=10,
    save_strategy="epoch",
    remove_unused_columns=False,
)

# =========================
# TRAINER
# =========================
trainer = Trainer(
    model=model,
    train_dataset=dataset["train"],
    args=training_args,
)

# =========================
# TRAIN
# =========================
trainer.train()
