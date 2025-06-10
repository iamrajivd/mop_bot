import streamlit as st
import yaml
import os
from datetime import datetime

# Directory to save output files
SAVE_DIR = "generated_mops"
os.makedirs(SAVE_DIR, exist_ok=True)

# Load YAML template
def load_yaml(file):
    try:
        return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error loading template: {e}")
        return {}

# Generate a .txt MoP file
def generate_txt(data):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{data['title'].replace(' ', '_')}_{now}.txt"
    path = os.path.join(SAVE_DIR, fname)

    with open(path, "w") as f:
        f.write(f"Title: {data.get('title', 'N/A')}\n")
        f.write(f"Version: {data.get('version', 'N/A')}\n")
        f.write(f"Environment: {data.get('environment', 'N/A')}\n\n")
        f.write(f"Description:\n{data.get('description', '')}\n\n")
        
        f.write("Components:\n")
        for c in data.get("components", []):
            f.write(f"- {c}\n")

        f.write("\nProcedure Commands:\n")
        for cmd in data.get("commands", []):
            f.write(f"{cmd}\n")

        f.write("\nRollback Plan:\n")
        for step in data.get("rollback", []):
            f.write(f"{step}\n")

    return path

# Streamlit UI
st.set_page_config(page_title="Nokia CMM MoP Generator", layout="centered")
st.title("🧠 Nokia CMM MoP Bot (.txt Output Only)")

# Upload YAML template
uploaded_file = st.file_uploader("📂 Upload MoP YAML Template", type=["yaml"])

if uploaded_file:
    mop_data = load_yaml(uploaded_file)
    
    if mop_data:
        st.subheader("📝 MoP Preview")
        st.json(mop_data)

        if st.button("📄 Generate .txt MoP"):
            output_path = generate_txt(mop_data)
            st.success(f"✅ MoP .txt file saved at: {output_path}")
            with open(output_path, "rb") as f:
                st.download_button("📥 Download .txt", data=f, file_name=os.path.basename(output_path), mime="text/plain")
