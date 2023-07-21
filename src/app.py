import torch
import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration

# Carregar o tokenizer e modelo BART pré-treinado
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Função para gerar resumo com base no texto inserido pelo usuário
def generate_summary(text, max_length=100, temperature=0.8):
    inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True)

    # Realizar a inferência para gerar o resumo do texto
    with torch.no_grad():
        output = model.generate(
            inputs.input_ids,
            max_length=max_length,
            do_sample=True,
            temperature=temperature
        )

    # Decodificar o resumo gerado
    summary = tokenizer.decode(output[0], skip_special_tokens=True)

    return summary

# Configurar a interface do aplicativo Streamlit
st.title("Aplicativo de Resumo de Texto com BART")
text_input = st.text_area("Insira o texto para resumo aqui:")

if st.button("Gerar Resumo"):
    if text_input:
        summary = generate_summary(text_input)
        st.subheader("Resumo:")
        st.write(summary)
    else:
        st.warning("Insira um texto para gerar o resumo.")
