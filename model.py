import streamlit as st
from nanonets import NANONETSOCR
import io
import os

def process_file(file_path):
    model = NANONETSOCR()
    model.set_token('95e09787-0a63-11ee-9c73-1e85f057e35b')
    pred_json = model.convert_to_prediction(uploaded_file.name)
    value1 = pred_json['results'][0]['page_data'][0]['words']
    extracted_text = []
    for item in value1:
        if 'text' in item:
            extracted_text.append({'key': item['text']})
    value = pred_json['results'][0]['page_data'][0]['raw_text']

    my_string = ' '.join(str(item) for item in extracted_text)

    converted_text = my_string + "\n" + value
    return converted_text


st.title('PDF to JSON Converter')

uploaded_file = st.file_uploader("Choose a file", type='pdf')
if uploaded_file is not None:
    file_name = uploaded_file.name
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'wb') as file:
        file.write(uploaded_file.getvalue())
    
    st.write("Selected File:", file_name)
    
    if st.button("Process File"):
        result = process_file(file_path)
        st.write(result)

        def generate_text():
            bytes_io = io.BytesIO()
            bytes_io.write(result.encode())
            bytes_io.seek(0)
            return bytes_io
        
        bytes_io = generate_text()
        st.download_button("Download", bytes_io, file_name="output.txt", mime="text/plain")
