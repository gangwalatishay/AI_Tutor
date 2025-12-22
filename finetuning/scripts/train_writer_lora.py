from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model

BASE_MODEL = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    load_in_8bit=True,
    device_map="auto"
)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL
)

dataset = load_dataset("json", data_files="../data/writer.jsonl")

args = TrainingArguments(
    output_dir="../adapters/writer_lora",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=False,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    train_dataset=dataset["train"],
    args=args
)

trainer.train()
