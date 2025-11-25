import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Verificador de Processos ")

st.title("Verificador de Processos Judiciais")

content = st.text_area("Conteúdo (texto ou JSON)", height=200)

api_url = os.getenv("API_URL", "http://localhost:8000")

st.subheader("Resposta da LLM")
response_box = st.empty()

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Enviar"):
        if not content:
            st.warning("Preencha o campo de conteúdo antes de enviar.")
        else:
            payload = {"content": content}
            try:
                with st.spinner("Enviando para /query e aguardando resposta..."):
                    resp = requests.post(f"{api_url}/query", json=payload, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                
                if isinstance(data, dict) and "response" in data:
                    response_box.json({"response": data.get("response")})
                else:
                    response_box.json(data)
            except Exception as e:
                response_box.error(f"Erro ao conectar com o backend: {e}")

st.markdown("---")