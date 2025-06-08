import streamlit as st
import yaml
from datetime import datetime
from word_exporter import generate_word
from pdf_exporter import export_to_pdf
import os, json

st.set_page_config(page_title="Telecom MoP Generator", layout="wide")
st.title("📡 Telecom MoP Generator – Nokia Edition")

node = st.selectbox("Select Node Type", ["MME", "PCRF", "PGW", "AMF", "SMF"])
change_type = st.selectbox("Change Type", ["Software Upgrade", "Config Change", "License Update"])

mop_title = st.text_input("MoP Title", f"{node} - {change_type} - {datetime.now().strftime('%d-%b-%Y')}")
summary = st.text_area("Summary", "e.g. Software upgrade from v20.5 to v21.1")
pre_checks = st.text_area("Pre-Checks", "e.g. show status, check alarms")
procedure = st.text_area("Procedure Steps", "e.g. Upload ISO, verify checksum, upgrade")
rollback = st.text_area("Rollback Plan", "e.g. Reboot node, restore config")
post_checks = st.text_area("Post-Checks", "e.g. validate services, check logs")
approvals = st.text_area("Approvals", "e.g. NOC Manager, Change Manager")

if st.button("Generate Word MoP"):
    output_path = generate_word(title, description, version, components, commands)
    st.success(f"Word MoP generated: {output_path}")

if st.button("🧾 Export to PDF"):
    export_to_pdf(mop_title, node, change_type, summary, pre_checks, procedure, rollback, post_checks, approvals)
    
# Save MoP
if st.button("💾 Save MoP"):
    if not os.path.exists("saved_mops"):
        os.makedirs("saved_mops")
    mop_data = {
        "mop_title": mop_title, "node": node, "change_type": change_type,
        "summary": summary, "pre_checks": pre_checks, "procedure": procedure,
        "rollback": rollback, "post_checks": post_checks, "approvals": approvals
    }
    with open(f"saved_mops/{mop_title.replace(' ', '_')}.json", "w") as f:
        json.dump(mop_data, f)
    st.success("MoP Saved!")

# Load MoP
saved_files = os.listdir("saved_mops") if os.path.exists("saved_mops") else []
selected_file = st.selectbox("📂 Load Saved MoP", [""] + saved_files)
if selected_file:
    with open(f"saved_mops/{selected_file}", "r") as f:
        data = json.load(f)
        mop_title = data["mop_title"]
        node = data["node"]
        change_type = data["change_type"]
        summary = data["summary"]
        pre_checks = data["pre_checks"]
        procedure = data["procedure"]
        rollback = data["rollback"]
        post_checks = data["post_checks"]
        approvals = data["approvals"]
        st.experimental_rerun()

import yaml

with open("nokia_commands.yaml", "r") as f:
    commands_data = yaml.safe_load(f)

all_components = list(commands_data.keys())
components = st.multiselect("Select Components", all_components)
selected_commands = []

for component in components:
    cmds = st.multiselect(f"{component} Commands", commands_data[component], key=component)
    selected_commands.extend(cmds)
