import streamlit as st
from nanonets import NANONETSOCR
import io


def process_file(uploaded_file):
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
    file_details = {"FileName": uploaded_file.name,
                    "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.write(file_details)
    result = process_file(uploaded_file)
    st.write(result)

    def generate_text():
        bytes_io = io.BytesIO()
        bytes_io.write(result.encode())
        bytes_io.seek(0)
        return bytes_io

if st.button("Download Text File"):
    bytes_io = generate_text()
    st.download_button("Download", bytes_io,
                       file_name="output.txt", mime="text/plain")
