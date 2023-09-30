import inspect
import textwrap
from datetime import datetime

import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from annotated_text import annotated_text

from demo_echarts import ST_DEMOS
from demo_pyecharts import ST_PY_DEMOS
from streamlit_echarts import st_echarts

from gtts import gTTS
from io import BytesIO

from pathlib import Path
import json
import re

import pandas as pd

from PIL import Image
# You can always call this function where ever you want
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

language_code_to_name = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",  # Add more language codes and names as needed
}

def load_patient_data(patient_id):
    # Construct the JSON file path based on the extracted patient ID
    json_file_path = f"./data/Themes_2&4_Visualization_and_Summarization/Specific_Encounter_Examples/{patient_id}.json"
    
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)

def display_reason_for_referral(reason_for_referral):
    # Create two columns for displaying data
    # Display header information
    st.subheader("Referral History")
    st.write(reason_for_referral['text'], unsafe_allow_html=True)
        
def display_header_info(header):
    # Create two columns for displaying data
    col1, col2 = st.columns(2)

    # Display header information
    with col1:
        st.markdown("#### Admission Information")
        # st.write(f"Title: {header['title']}")
        doa_date = header['date_time']['point']['date']
        formatted_doa = datetime.strptime(doa_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Date of Admission:{formatted_doa}")
        # st.write(f"Date Time Precision: {header['date_time']['point']['precision']}")
        st.write(f"Author: {header['author']['author'][0]['name'][0]['prefix']} {header['author']['author'][0]['name'][0]['first']} {header['author']['author'][0]['name'][0]['last']}")
        st.write(f"Organization: {header['author']['author'][0]['organization'][0]['name'][0]}")
        st.write(f"Phone: {header['author']['author'][0]['phone'][0]['number']}")
        st.write(f"Email: {header['author']['author'][0]['email'][0]['address']}")
        st.write(f"Doctor Identifier: {header['author']['author'][0]['identifiers'][0]['identifier']}")

    with col2:
        st.markdown("#### Admission Identifiers")
        # st.write(f"Admission Identifier: {header['identifiers'][0]['identifier']}")
        st.write(f"Confidentiality Code: {header['confidentiality_code']['code']}")
        st.write(f"Confidentiality Code Name: {header['confidentiality_code']['name']}")
        st.write(f"Code: {header['code']['code']}")
        st.write(f"Code Name: {header['code']['name']}")
        # st.write(f"Template: {header['template']}")
    
    with col1:
        st.markdown("#### Custodian")
        st.write(f"Custodian: {header['custodian']['name'][0]}")
        st.write(f"Custodian Phone: {header['custodian']['phone'][0]['number']}")
    
    with col2:
        st.markdown("#### Service Data")
        dos_lowdate = header['service_event']['date_time']['low']['date']
        formatted_dos_low = datetime.strptime(dos_lowdate, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Service Start Event Date:{formatted_doa}")
        # st.write(f"Service Event Date Time Low: {header['service_event']['date_time']['low']['date']}")
        
        # st.write(f"Service Event Date Time Low Precision: {header['service_event']['date_time']['low']['precision']}")
        dos_highdate = header['service_event']['date_time']['low']['date']
        formatted_dos_high = datetime.strptime(dos_highdate, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Service End Event Date:{formatted_doa}")
        # st.write(f"Service Event Date Time High: {header['service_event']['date_time']['high']['date']}")
        
        # st.write(f"Service Event Date Time High Precision: {header['service_event']['date_time']['high']['precision']}")
        st.write(f"Performer Identifier: {header['service_event']['performer'][0]['performer'][0]['identifiers'][0]['identifier']}")

def display_demographics(demographics_data):
    add_vertical_space(1)
    colored_header(
        label=f"Patient Information",
        description=f"",
        color_name="blue-70",
    )
    
    # Create two columns for displaying data
    col1, col2 = st.columns(2)
    
    # Display Name
    with col1:
        st.markdown("##### Name")
        st.write(f"Last Name: {demographics_data['name']['last']}" + f" First Name: {demographics_data['name']['first']}")

    # Display Date of Birth
    with col2:
        st.markdown("##### Date of Birth")
        dob_date = demographics_data['dob']['point']['date']
        formatted_dob = datetime.strptime(dob_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
        st.write(f"{formatted_dob}")
        # st.write(f"Date of Birth Precision: {demographics_data['dob']['point']['precision']}")

    # Display Gender
    with col1:
        st.markdown("##### Gender")
        st.write(f"{demographics_data['gender']['name'].upper()}")
        # st.write(f"Gender Code: {demographics_data['gender']['code']}")
        # st.write(f"Gender Code System Name: {demographics_data['gender']['code_system_name']}")

    # Display Identifiers
    with col2:
        st.markdown("##### Identifiers")
        for identifier in demographics_data['identifiers']:
            # st.write(f"Identifier: {identifier['identifier']}")
            st.write(f"Extension: {identifier['extension']}")

    # Display Address
    with col1:
        st.markdown("##### Address")
        for address in demographics_data['addresses']:
            if 'street_lines' not in address:
                address['street_lines'] = ['No Address Found']
            for street_lines in address['street_lines']:
                st.write(f"{street_lines}")
            st.write(f"City: {address['city']}")
            st.write(f"State: {address['state']}")
            if 'zip' not in address:
                address['zip'] = 'No Zip Code Found'
            st.write(f"ZipCode: {address['zip']}")
            st.write(f"Country: {address['country']}")
            # st.write(f"Use: {address['use']}")

    # Display Phone
    with col2:
        st.markdown("##### Contact")
        if 'phone' not in demographics_data:
            demographics_data['phone'] = []
        for phone in demographics_data['phone']:
            st.write(f"Number: {phone['number']}")
            st.write(f"Type: {phone['type']}")

    # Display Email
    with col2:
        for email in demographics_data['email']:
            st.write(f"Email Address: {email['address']}")

    # Display Race
    with col1:
        st.markdown("##### Race")
        # st.write(f"Race Code: {demographics_data['race']['code']}")
        # st.write(f"Race Code System Name: {demographics_data['race']['code_system_name']}")
        st.write(f"Race Name: {demographics_data['race']['name']}")

    # Display Ethnicity
    with col2:
        st.markdown("##### Ethnicity")
        # st.write(f"Ethnicity Code: {demographics_data['ethnicity']['code']}")
        # st.write(f"Ethnicity Code System Name: {demographics_data['ethnicity']['code_system_name']}")
        st.write(f"Ethnicity Name: {demographics_data['ethnicity']['name']}")

    # Display Languages
    with col2:
        st.markdown("##### Languages")
        for language in demographics_data['languages']:
            language_code = language['language']['code']
            language_name = language_code_to_name.get(language_code, "Unknown")
            st.write(f"Language Known: {language_name}")

def display_vitals(data):
    # Create an empty list to store DataFrames for each Vital Name
    vitals_dataframes = []

    # Loop through vitals and extract data
    for vital in data:
        
        if "date_time" in vital and "point" in vital["date_time"]:
            date_precision = vital["date_time"]["point"]["precision"]
            # Format date based on precision
            if date_precision == "day":
                date = pd.to_datetime(vital["date_time"]["point"]["date"]).strftime("%d-%m-%y")
                
            elif date_precision == "hour":
                date = pd.to_datetime(vital["date_time"]["point"]["date"]).strftime("%d-%m-yy %H:%M")
        else:
            date = "NA"

        if "vital" in vital and "name" in vital["vital"] and "value" in vital:
            vital_name = vital["vital"]["name"]
            value = vital["value"]
        
            # Create a DataFrame for each Vital Name
            df = pd.DataFrame({"Date": [date], "Value": [value]})
            df["Vital Name"] = vital_name
            if value != 0.0:
                vitals_dataframes.append(df)

    if len(vitals_dataframes) != 0:
        # Concatenate all DataFrames
        combined_data = pd.concat(vitals_dataframes, ignore_index=True)

        # Create a graph for each Vital Name
        for vital_name in combined_data["Vital Name"].unique():
            st.subheader(vital_name)
            filtered_data = combined_data[combined_data["Vital Name"] == vital_name]
            st.line_chart(filtered_data.set_index("Date"))

def display_results(result_data):
    df = None
    for data in result_data:
        if 'results' in data:
            for res_data in data['results']:
                if "date_time" in res_data:
                    # Create a DataFrame for the given result data
                    date = pd.to_datetime(res_data['date_time']['low']['date'])
                    date_precision = res_data['date_time']['low']['precision']
                    formatted_date = "NA"
                    # Format date based on precision
                    if date_precision == 'day':
                        formatted_date = date.strftime('%d-%m-%y')
                    elif date_precision == 'hour':
                        formatted_date = date.strftime('%d-%m-yy %H:%M')

                    result_name = res_data['result']['name']
                    if 'value' in res_data:
                        value = res_data['value']
                    else:
                        value = "NA"
                    
                    # Create a DataFrame
                    df = pd.DataFrame({'Date': [formatted_date], 'Value': [value]})
                    df['Result Name'] = result_name
    if df is not None:
        # Display a line chart for the result
        st.subheader("Test Results")
        st.line_chart(df.set_index('Date'))

def display_medications(medication_data):
    # Create an empty list to store the medication data as dictionaries
    medication_list = []

    # Iterate through the list of medication data and format it
    for med_data in medication_data:
        if 'date_time' in med_data:
            date = pd.to_datetime(med_data['date_time']['low']['date'])
            date_precision = med_data['date_time']['low']['precision']
            # Format date based on precision
            if date_precision == 'day':
                formatted_date = date.strftime('%d-%m-%y')
            elif date_precision == 'hour':
                formatted_date = date.strftime('%d-%m-yy %H:%M')

        else:
            formatted_date = "NA"


        status = med_data['status']
        sig = med_data['sig']
        product_name = med_data['product']['product']['name']
        if 'route' in med_data['administration']:
            route = med_data['administration']['route']['name']
        else:
            route = 'NA'
        if 'dose' in med_data['administration']:
            dose = med_data['administration']['dose']['value']
        else:
            dose = 'NA'

        # Append the formatted medication data as a dictionary to the list
        medication_list.append({
            'Date': formatted_date,
            'Status': status,
            'SIG': sig,
            'Product Name': product_name,
            'Route': route,
            'Dose': dose
        })
    # Remove duplicates from medication_list
    # Create a temporary set to keep track of seen dictionaries
    seen = set()
    # Create a new list for unique dictionaries
    unique_medication_list = []
    # Loop through the original list and append only unique dictionaries to the new list
    for medication in medication_list:
        # Convert the dictionary to a frozenset to make it hashable and store it in the 'seen' set
        medication_set = frozenset(medication.items())
        if medication_set not in seen:
            seen.add(medication_set)
            unique_medication_list.append(medication)
    if(len(medication_list) != 0):
        medication_df = pd.DataFrame(unique_medication_list)
        st.subheader("Medications Details")
        st.table(medication_df)

def display_encounters(encounter_data):
    # Create an empty list to store the encounter data as dictionaries
    encounter_list = []

    # Iterate through the list of encounter data and format it
    for enc_data in encounter_data:        
        if 'date_time' in enc_data:
            date = pd.to_datetime(enc_data['date_time']['low']['date'])
            date_precision = enc_data['date_time']['low']['precision']
            # Format date based on precision
            if date_precision == 'day':
                formatted_date = date.strftime('%d-%m-%y')
            elif date_precision == 'hour':
                formatted_date = date.strftime('%d-%m-yy %H:%M')

        else:
            formatted_date = "NA"

        encounter_reason = enc_data['encounter']

        if(encounter_reason != {}):
            # Append the formatted encounter data as a dictionary to the list
            encounter_list.append({
                'Date': formatted_date,
                'Encounter Reason': encounter_reason,
            })

    if len(encounter_list) != 0:
        # Create a DataFrame from the list of medication dictionaries
        encounter_df = pd.DataFrame(encounter_list)
        # Display the medication data as a table in Streamlit
        st.subheader("Encounter Details")
        st.table(encounter_df)

def display_allergy(allergy_data):
    # Create a list of dictionaries to hold the data
    allergy_list = []

    # Populate the list of dictionaries
    for item in allergy_data:
        observation = item.get('observation', {})
        negation_indicator = observation.get('negation_indicator', None) 
        intolerance = observation.get('intolerance', {})
        status = observation.get('status', {})
        allergy_list.append({
            'Negation Indicator': negation_indicator,
            'Intolerance Name': intolerance['name'],
            'Intolerance Code': intolerance['code'],
            'Intolerance Code System': intolerance['code_system_name'],
            'Status Name': status['name'],
            'Status Code': status['code'],
            'Status Code System': status['code_system_name'],
        })

    if len(allergy_list) != 0:
        allergy_df = pd.DataFrame(allergy_list)
        st.subheader("Allergy Details")
        st.table(allergy_df)

def display_immunizations(immunizations_data):
    # Create a list of dictionaries to hold the data
    immunization_list = []
    for immunization in immunizations_data:
        if "date_time" in immunization and "point" in immunization["date_time"]:
            
            date_precision = immunization["date_time"]["point"]["precision"]
            # Format date based on precision
            if date_precision == "day":
                date = pd.to_datetime(immunization["date_time"]["point"]["date"]).strftime("%d-%m-%y")
                
            elif date_precision == "hour":
                date = pd.to_datetime(immunization["date_time"]["point"]["date"]).strftime("%d-%m-yy %H:%M")
        else:
            date = "NA"
        if "product" in immunization and "product" in immunization["product"]:
            immunization_name = immunization["product"]["product"]["name"]
            
            immunization_list.append({
                'Date': date,
                'Product': immunization_name,
            })
    if len(immunization_list) != 0:
        immunization_df = pd.DataFrame(immunization_list)
        st.subheader("Immunization Details")
        st.table(immunization_df)

def display_problems(problems_data):
    problems_list = []
    for problem in problems_data:
        if 'date_time' in problem:
            date = pd.to_datetime(problem['date_time']['low']['date'])
            date_precision = problem['date_time']['low']['precision']
            # Format date based on precision
            if date_precision == 'day':
                formatted_date = date.strftime('%d-%m-%y')
            elif date_precision == 'hour':
                formatted_date = date.strftime('%d-%m-yy %H:%M')

        else:
            formatted_date = "NA"
        if 'problem' in problem and 'code' in problem['problem']:
            problem_name = problem['problem']['code']['name']
            problem_code = problem['problem']['code']['code']
            problem_code_system = problem['problem']['code']['code_system_name']
            problems_list.append({
                'Date': formatted_date,
                'Problem Name': problem_name,
                'Problem Code': problem_code,
                'Problem Code System': problem_code_system,
            })
    # Remove duplicates from problems_list
    # Create a temporary set to keep track of seen dictionaries
    seen = set()
    # Create a new list for unique dictionaries
    unique_problems_list = []
    # Loop through the original list and append only unique dictionaries to the new list
    for problem in problems_list:
        # Convert the dictionary to a frozenset to make it hashable and store it in the 'seen' set
        problem_set = frozenset(problem.items())
        if problem_set not in seen:
            seen.add(problem_set)
            unique_problems_list.append(problem)
    if(len(problems_list) != 0):
        problems_df = pd.DataFrame(unique_problems_list)
        st.subheader("Problem Details")
        st.table(problems_df)
        
def display_procedures(procedures_data):
    procedure_list = []
    for procedure in procedures_data:
        if 'date_time' in procedure:
            date = pd.to_datetime(procedure['date_time']['low']['date'])
            date_precision = procedure['date_time']['low']['precision']
            # Format date based on precision
            if date_precision == 'day':
                formatted_date = date.strftime('%d-%m-%y')
            elif date_precision == 'hour':
                formatted_date = date.strftime('%d-%m-yy %H:%M')

        else:
            formatted_date = "NA"
        if 'procedure' in procedure and 'code' in procedure['procedure']:
            procedure_name = procedure['procedure']['name']
            procedure_code = procedure['procedure']['code']
            procedure_code_system = procedure['procedure']['code_system_name']
            procedure_list.append({
                'Date': formatted_date,
                'Problem Name': procedure_name,
                'Problem Code': procedure_code,
                'Problem Code System': procedure_code_system,
            })
    if(len(procedure_list) != 0):
        procedure_df = pd.DataFrame(procedure_list)
        st.subheader("Procedure Details")
        st.table(procedure_df)
            
def display_plan_of_care(plan_of_care_data):
    # Create a list of dictionaries to hold the data
    plan_of_care_list = []
    for plan_of_care in plan_of_care_data:
        if "date_time" in plan_of_care and "point" in plan_of_care["date_time"]:
            
            date_precision = plan_of_care["date_time"]["point"]["precision"]
            # Format date based on precision
            if date_precision == "day":
                date = pd.to_datetime(plan_of_care["date_time"]["point"]["date"]).strftime("%d-%m-%y")
                
            elif date_precision == "hour":
                date = pd.to_datetime(plan_of_care["date_time"]["point"]["date"]).strftime("%d-%m-yy %H:%M")
        else:
            date = "NA"
        if "plan" in plan_of_care and "code" in plan_of_care["plan"]:
            plan_of_care_name = plan_of_care["plan"]["name"]
            plan_of_care_code = plan_of_care["plan"]["code"]
            if plan_of_care_code != 'NI':
                plan_of_care_list.append({
                    'Date': date,
                    'Product': plan_of_care_name,
                })
    if len(plan_of_care_list) != 0:
        plan_of_care_df = pd.DataFrame(plan_of_care_list)
        st.subheader("Plan of Care Details")
        st.table(plan_of_care_df)

def display_patient_info(data):
    patient_data = data['data']
    # Display patient information here
    colored_header(
        label=f"{patient_data['header']['title']}",
        description=f"ID: {patient_data['header']['identifiers'][0]['identifier']}",
        color_name="blue-70",
    )
    

    display_demographics(patient_data['demographics'])
    st.markdown("""---""")
    display_header_info(patient_data['header'])
    st.markdown("""---""")
    display_reason_for_referral(patient_data['reason_for_referral'])
    st.markdown("""---""")
    display_vitals(patient_data['vitals'])
    st.markdown("""---""")
    display_results(patient_data['results'])
    st.markdown("""---""")
    display_medications(patient_data['medications'])
    st.markdown("""---""")
    display_encounters(patient_data['encounters'])
    st.markdown("""---""")
    display_allergy(patient_data['allergies'])
    st.markdown("""---""")
    display_immunizations(patient_data['immunizations'])
    st.markdown("""---""")
    display_problems(patient_data['problems'])
    st.markdown("""---""")
    display_procedures(patient_data['procedures'])
    st.markdown("""---""")
    display_plan_of_care(patient_data['plan_of_care'])
    st.markdown("""---""")
    # liquidfill_option = {
    #     "series": [{"type": "liquidFill", "data": [0.6, 0.5, 0.4, 0.3]}]
    # }
    # st_echarts(liquidfill_option)

def generate_summary_100_words(patient_data):
    # Create a 100-word summary template
    summary_template = (
        "Patient {first_name} {last_name} ({gender}), born on {dob}, was admitted on {admission_date} "
        "at {admission_time} by Dr. {doctor_name} from {organization}. "
        "The patient's contact number is {contact_number} and email address is {email}. "
        "Patient's ID is {patient_id}. The patient's address is {street}, {city}, {state}, {zipcode}, {country}. "
        "The patient's race is {race}. The patient's ethnicity is {ethnicity}. "
        "Languages known: {languages}. Confidentiality code: {confidentiality_code}. "
        "The service started on {service_start_date} and ended on {service_end_date}."
    )

    placeholder_pattern = r"{(\w+)}"
    placeholders = re.findall(placeholder_pattern, summary_template)
    # Initialize the start index of the text
    start_index = 0

    # Create a list to store the annotations
    annotations = []

    # Iterate through placeholders and add annotations
    for placeholder in placeholders:
        # Find the index of the placeholder in the template
        placeholder_index = summary_template.index("{" + placeholder + "}")
        
        # Get the text before the placeholder
        text_before = summary_template[start_index:placeholder_index]
        
        if text_before:
            text_before_annotated = (text_before,'')
            annotations.append(text_before)  # Add normal text
        
        # Add the placeholder as an annotation
        # annotations.append(("{" + placeholder + "}", f"{{{placeholder}}}"))
        annotations.append(("{" + "}", f"{placeholder}"))
        
        # Update the start index for the next iteration
        start_index = placeholder_index + len("{" + placeholder + "}")

    # Add any remaining text after the last placeholder
    text_after = summary_template[start_index:]
    if text_after:
        text_after_annotated = (text_after,'')
        annotations.append(text_after)

    # Fill in the patient data
    summary = summary_template.format(
        first_name=patient_data['demographics']['name']['first'],
        last_name=patient_data['demographics']['name']['last'],
        gender=patient_data['demographics']['gender']['name'],
        dob=patient_data['demographics']['dob']['point']['date'][:10],
        admission_date=patient_data['header']['date_time']['point']['date'][:10],
        admission_time=patient_data['header']['date_time']['point']['date'].split('T')[1][:8],
        doctor_name=patient_data['header']['author']['author'][0]['name'][0]['last'],
        organization=patient_data['header']['author']['author'][0]['organization'][0]['name'][0],
        contact_number= patient_data['demographics']['phone'][0]['number'] if 'phone' in patient_data['demographics'] and patient_data['demographics']['phone'][0].get('number') else ' ',
        email=patient_data['demographics']['email'][0]['address'],
        patient_id=patient_data['header']['identifiers'][0]['identifier'],
        street=patient_data['demographics']['addresses'][0]['street_lines'][0] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'street_lines' in patient_data['demographics']['addresses'][0] else '',
        city=patient_data['demographics']['addresses'][0]['city'],
        state=patient_data['demographics']['addresses'][0]['state'],
        zipcode=patient_data['demographics']['addresses'][0]['zip'] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'zip' in patient_data['demographics']['addresses'][0] else ' ',
        country=patient_data['demographics']['addresses'][0]['country'],
        race=patient_data['demographics']['race']['name'],
        ethnicity=patient_data['demographics']['ethnicity']['name'],
        languages=', '.join(lang['language']['code'] for lang in patient_data['demographics']['languages']),
        confidentiality_code=patient_data['header']['confidentiality_code']['code'],
        service_start_date=patient_data['header']['service_event']['date_time']['low']['date'][:10],
        service_end_date=patient_data['header']['service_event']['date_time']['high']['date'][:10],
    )
    data = {
        'first_name': patient_data['demographics']['name']['first'],
        'last_name': patient_data['demographics']['name']['last'],
        'gender': patient_data['demographics']['gender']['name'],
        'dob': patient_data['demographics']['dob']['point']['date'][:10],
        'admission_date': patient_data['header']['date_time']['point']['date'][:10],
        'admission_time': patient_data['header']['date_time']['point']['date'].split('T')[1][:8],
        'doctor_name': patient_data['header']['author']['author'][0]['name'][0]['last'],
        'organization': patient_data['header']['author']['author'][0]['organization'][0]['name'][0],
        'contact_number': patient_data['demographics']['phone'][0]['number'] if 'phone' in patient_data['demographics'] and patient_data['demographics']['phone'][0].get('number') else ' ',
        'email': patient_data['demographics']['email'][0]['address'],
        'patient_id': patient_data['header']['identifiers'][0]['identifier'],
        'street': patient_data['demographics']['addresses'][0]['street_lines'][0] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'street_lines' in patient_data['demographics']['addresses'][0] else '',
        'city': patient_data['demographics']['addresses'][0]['city'],
        'state': patient_data['demographics']['addresses'][0]['state'],
        'zipcode': patient_data['demographics']['addresses'][0]['zip'] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'zip' in patient_data['demographics']['addresses'][0] else ' ',
        'country': patient_data['demographics']['addresses'][0]['country'],
        'race': patient_data['demographics']['race']['name'],
        'ethnicity': patient_data['demographics']['ethnicity']['name'],
        'languages': ', '.join(lang['language']['code'] for lang in patient_data['demographics']['languages']),
        'confidentiality_code': patient_data['header']['confidentiality_code']['code'],
        'service_start_date': patient_data['header']['service_event']['date_time']['low']['date'][:10],
        'service_end_date': patient_data['header']['service_event']['date_time']['high']['date'][:10],
    }

    filled_annotations = []
    for text_or_tuple in annotations:
        if isinstance(text_or_tuple, tuple):
            text, label = text_or_tuple
            filled_annotations.append((text.format(data.get(label, "")), label))
        else:
            filled_annotations.append((text_or_tuple, ""))
    
    with st.expander("SHORT SUMMARIZE"):
        # Display the formatted summary using annotated_text
        annotated_text(*filled_annotations)
        
        sound_file = BytesIO()
        tts = gTTS(summary, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)

def generate_summary_200_words(patient_data, vitals_str):
    # Create a 200-word summary template
    summary_template = (
        "Patient {first_name} {last_name} ({gender}), born on {dob}, was admitted on {admission_date} "
        "at {admission_time} by Dr. {doctor_name} from {organization}. "
        "The patient's contact number is {contact_number} and email address is {email}. "
        "Patient's ID is {patient_id}. The patient's address is {street}, {city}, {state}, {zipcode}, {country}. "
        "The patient's race is {race}. The patient's ethnicity is {ethnicity}. "
        "Languages known: {languages}. Confidentiality code: {confidentiality_code}. "
        "The service started on {service_start_date} and ended on {service_end_date}. "
        "Vitals: {vitals}. Last Medications are {medications}."
    )
    placeholder_pattern = r"{(\w+)}"
    placeholders = re.findall(placeholder_pattern, summary_template)
    # Initialize the start index of the text
    start_index = 0

    # Create a list to store the annotations
    annotations = []

    # Iterate through placeholders and add annotations
    for placeholder in placeholders:
        # Find the index of the placeholder in the template
        placeholder_index = summary_template.index("{" + placeholder + "}")
        
        # Get the text before the placeholder
        text_before = summary_template[start_index:placeholder_index]
        
        if text_before:
            annotations.append(text_before)  # Add normal text
        
        # Add the placeholder as an annotation
        # annotations.append(("{" + placeholder + "}", f"{{{placeholder}}}"))
        annotations.append(("{" + "}", f"{placeholder}"))
        
        # Update the start index for the next iteration
        start_index = placeholder_index + len("{" + placeholder + "}")

    # Add any remaining text after the last placeholder
    text_after = summary_template[start_index:]
    if text_after:
        annotations.append(text_after)

    # Fill in the patient data
    summary = summary_template.format(
        first_name=patient_data['demographics']['name']['first'],
        last_name=patient_data['demographics']['name']['last'],
        gender=patient_data['demographics']['gender']['name'],
        dob=patient_data['demographics']['dob']['point']['date'][:10],
        admission_date=patient_data['header']['date_time']['point']['date'][:10],
        admission_time=patient_data['header']['date_time']['point']['date'].split('T')[1][:8],
        doctor_name=patient_data['header']['author']['author'][0]['name'][0]['last'],
        organization=patient_data['header']['author']['author'][0]['organization'][0]['name'][0],
        contact_number=patient_data['demographics']['phone'][0]['number'] if 'phone' in patient_data['demographics'] and patient_data['demographics']['phone'][0].get('number') else ' ',
        email=patient_data['demographics']['email'][0]['address'],
        patient_id=patient_data['header']['identifiers'][0]['identifier'],
        street=patient_data['demographics']['addresses'][0]['street_lines'][0] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'street_lines' in patient_data['demographics']['addresses'][0] else '',
        city=patient_data['demographics']['addresses'][0]['city'],
        state=patient_data['demographics']['addresses'][0]['state'],
        zipcode=patient_data['demographics']['addresses'][0]['zip'] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'zip' in patient_data['demographics']['addresses'][0] else ' ',
        country=patient_data['demographics']['addresses'][0]['country'],
        race=patient_data['demographics']['race']['name'],
        ethnicity=patient_data['demographics']['ethnicity']['name'],
        languages=', '.join(lang['language']['code'] for lang in patient_data['demographics']['languages']),
        confidentiality_code=patient_data['header']['confidentiality_code']['code'],
        service_start_date=patient_data['header']['service_event']['date_time']['low']['date'][:10],
        service_end_date=patient_data['header']['service_event']['date_time']['high']['date'][:10],
        vitals= vitals_str,
        medications = ' '.join(set(med['product']['product']['name'] for med in patient_data.get('medications', []) ))
    )
    data = {
        'first_name': patient_data['demographics']['name']['first'],
        'last_name': patient_data['demographics']['name']['last'],
        'gender': patient_data['demographics']['gender']['name'],
        'dob': patient_data['demographics']['dob']['point']['date'][:10],
        'admission_date': patient_data['header']['date_time']['point']['date'][:10],
        'admission_time': patient_data['header']['date_time']['point']['date'].split('T')[1][:8],
        'doctor_name': patient_data['header']['author']['author'][0]['name'][0]['last'],
        'organization': patient_data['header']['author']['author'][0]['organization'][0]['name'][0],
        'contact_number': patient_data['demographics']['phone'][0]['number'] if 'phone' in patient_data['demographics'] and patient_data['demographics']['phone'][0].get('number') else ' ',
        'email': patient_data['demographics']['email'][0]['address'],
        'patient_id': patient_data['header']['identifiers'][0]['identifier'],
        'street': patient_data['demographics']['addresses'][0]['street_lines'][0] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'street_lines' in patient_data['demographics']['addresses'][0] else '',
        'city': patient_data['demographics']['addresses'][0]['city'],
        'state': patient_data['demographics']['addresses'][0]['state'],
        'zipcode': patient_data['demographics']['addresses'][0]['zip'] if 'addresses' in patient_data['demographics'] and len(patient_data['demographics']['addresses']) > 0 and 'zip' in patient_data['demographics']['addresses'][0] else ' ',
        'country': patient_data['demographics']['addresses'][0]['country'],
        'race': patient_data['demographics']['race']['name'],
        'ethnicity': patient_data['demographics']['ethnicity']['name'],
        'languages': ', '.join(lang['language']['code'] for lang in patient_data['demographics']['languages']),
        'confidentiality_code': patient_data['header']['confidentiality_code']['code'],
        'service_start_date': patient_data['header']['service_event']['date_time']['low']['date'][:10],
        'service_end_date': patient_data['header']['service_event']['date_time']['high']['date'][:10],
        'vitals': vitals_str,
        'medications': ' '.join(set(med['product']['product']['name'] for med in patient_data.get('medications', [])))
    }
    filled_annotations = []
    for text_or_tuple in annotations:
        if isinstance(text_or_tuple, tuple):
            text, label = text_or_tuple
            filled_annotations.append((text.format(data.get(label, "")), label))
        else:
            filled_annotations.append((text_or_tuple, ""))
    
    with st.expander("MEDIUM SUMMARIZE"):
        # Display the formatted summary using annotated_text
        annotated_text(*filled_annotations)
        
        sound_file = BytesIO()
        tts = gTTS(summary, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)

def generate_summary_500_words(patient_data, vitals_str):

    # Create a 500-word summary template
    summary_template = (
        "Patient {first_name} {last_name} ({gender}), born on {dob}, was admitted on {admission_date} "
        "at {admission_time} by Dr. {doctor_name} from {organization}. "
        "The service started on {service_start_date} and ended on {service_end_date}. "
        "Vitals: {vitals}. Last Medications are  {medications}. "
        "Allergies: {allergies}. Problems: {problems}. Procedures: {procedures}. "
    )
    placeholder_pattern = r"{(\w+)}"
    placeholders = re.findall(placeholder_pattern, summary_template)
    # Initialize the start index of the text
    start_index = 0

    # Create a list to store the annotations
    annotations = []

    # Iterate through placeholders and add annotations
    for placeholder in placeholders:
        # Find the index of the placeholder in the template
        placeholder_index = summary_template.index("{" + placeholder + "}")
        
        # Get the text before the placeholder
        text_before = summary_template[start_index:placeholder_index]
        
        if text_before:
            annotations.append(text_before)  # Add normal text
        
        # Add the placeholder as an annotation
        # annotations.append(("{" + placeholder + "}", f"{{{placeholder}}}"))
        annotations.append(("{" + "}", f"{placeholder}"))
        
        # Update the start index for the next iteration
        start_index = placeholder_index + len("{" + placeholder + "}")

    # Add any remaining text after the last placeholder
    text_after = summary_template[start_index:]
    if text_after:
        annotations.append(text_after)    

    # Fill in the patient data
    summary = summary_template.format(
        first_name=patient_data['demographics']['name']['first'],
        last_name=patient_data['demographics']['name']['last'],
        gender=patient_data['demographics']['gender']['name'],
        dob=patient_data['demographics']['dob']['point']['date'][:10],
        admission_date=patient_data['header']['date_time']['point']['date'][:10],
        admission_time=patient_data['header']['date_time']['point']['date'].split('T')[1][:8],
        doctor_name=patient_data['header']['author']['author'][0]['name'][0]['last'],
        organization=patient_data['header']['author']['author'][0]['organization'][0]['name'][0],
        service_start_date=patient_data['header']['service_event']['date_time']['low']['date'][:10],
        service_end_date=patient_data['header']['service_event']['date_time']['high']['date'][:10],
        vitals=vitals_str,
        medications = ' '.join(set(med['product']['product']['name'] for med in patient_data.get('medications', []) )),
        allergies=', '.join(set(allergy['observation']['intolerance']['name'] for allergy in patient_data.get('allergies', []))),
        problems=', '.join(set(problem['problem']['code']['name'] for problem in patient_data.get('problems', []))),
        procedures=', '.join(set(procedure['procedure']['name'] for procedure in patient_data.get('procedures', []))),
    )

    data = {
        'first_name': patient_data['demographics']['name']['first'],
        'last_name': patient_data['demographics']['name']['last'],
        'gender': patient_data['demographics']['gender']['name'],
        'dob': patient_data['demographics']['dob']['point']['date'][:10],
        'admission_date': patient_data['header']['date_time']['point']['date'][:10],
        'admission_time': patient_data['header']['date_time']['point']['date'].split('T')[1][:8],
        'doctor_name': patient_data['header']['author']['author'][0]['name'][0]['last'],
        'organization': patient_data['header']['author']['author'][0]['organization'][0]['name'][0],
        'service_start_date': patient_data['header']['service_event']['date_time']['low']['date'][:10],
        'service_end_date': patient_data['header']['service_event']['date_time']['high']['date'][:10],
        'vitals': vitals_str,
        'medications': ' '.join(set(med['product']['product']['name'] for med in patient_data.get('medications', []))),
        'allergies': ', '.join(set(allergy['observation']['intolerance']['name'] for allergy in patient_data.get('allergies', []))),
        'problems': ', '.join(set(problem['problem']['code']['name'] for problem in patient_data.get('problems', []))),
        'procedures': ', '.join(set(procedure['procedure']['name'] for procedure in patient_data.get('procedures', [])))
    }
    filled_annotations = []
    for text_or_tuple in annotations:
        if isinstance(text_or_tuple, tuple):
            text, label = text_or_tuple
            filled_annotations.append((text.format(data.get(label, "")), label))
        else:
            filled_annotations.append((text_or_tuple, ""))
    
    with st.expander("DETAILED SUMMARIZE"):
        # Display the formatted summary using annotated_text
        annotated_text(*filled_annotations)
        
        sound_file = BytesIO()
        tts = gTTS(summary, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)




st.set_page_config(
        page_title="Health Insight", page_icon=":chart_with_upwards_trend:"
)


my_logo = add_logo(logo_path="./logo/Unknown.jpeg", width=500, height=400)
st.sidebar.image(my_logo)

def main():
    colored_header(
        label="Health Insight : Charmhealth Patient Clinical Summary",
        description="",
        color_name="violet-70",
    )

    add_vertical_space(3)

    directory = "./data/Themes_2&4_Visualization_and_Summarization/Specific_Encounter_Examples/"
    p = Path(directory)
    files = list(p.glob('**/*.json'))
    patient_ids = []
    for path_to_file in files:
        patient_ids.append(path_to_file.stem)

    
    with st.sidebar:
        st.header("Select Patient")
        # Extract the patient IDs in the desired format
        extracted_patient_ids = []
        for patient_id in patient_ids:
            match = re.search(r'(PAT\d+|CHARM\d+|\d+)_ClinicalSummary', patient_id)
            if match:
                extracted_patient_ids.append(match.group(1))

        # Create a dropdown to select a patient
        selected_patient_id = st.selectbox("Select a Patient ID", extracted_patient_ids)

    if not selected_patient_id:
        st.warning("Please select a patient from the dropdown.")
    else:
        # Reconstruct the full patient ID with underscores
        selected_full_patient_id = [patient_id for patient_id in patient_ids if selected_patient_id in patient_id][0]
        original_patient_data = load_patient_data(selected_full_patient_id)
        patient_data = original_patient_data.copy()
        
        display_patient_info(patient_data)
        with st.sidebar:
            st.markdown("---")
            st.markdown(
                '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/pp_spector">@pp_spector</a></h6>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div style="margin-top: 0.75em;"><a href="https://www.buymeacoffee.com/princep" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
                unsafe_allow_html=True,
            )
        
        vitals_list = original_patient_data['data'].get('vitals', [])
        vitals_info_list = []
        for vital in vitals_list:
            if vital['vital']['name'] in ['Height', 'Weight', 'Pulse Rate', 'BMI', 'SPO2', 'Temperature']:
                vitals_info = {
                    'name': vital['vital']['name'],
                    'value': vital.get('value', 'N/A'),
                    'unit': vital.get('unit', 'N/A')
                }
                vitals_info_list.append(vitals_info)
        
        # Extract the first occurrence of each vital
        height_info = next((v for v in vitals_info_list if v['name'] == 'Height'), None)
        weight_info = next((v for v in vitals_info_list if v['name'] == 'Weight'), None)
        pulse_rate_info = next((v for v in vitals_info_list if v['name'] == 'Pulse Rate'), None)
        bmi_info = next((v for v in vitals_info_list if v['name'] == 'BMI'), None)
        spo2_info = next((v for v in vitals_info_list if v['name'] == 'SPO2'), None)
        temperature_info = next((v for v in vitals_info_list if v['name'] == 'Temperature'), None)
        
        height_str = f"Last Height is  {height_info['value']} cm " if height_info else ''
        weight_str = f"Last Weight is {weight_info['value']} kg " if weight_info else ''
        pulse_rate_str = f"Last Pulse Rate is {pulse_rate_info['value']} " if pulse_rate_info else ''
        bmi_str = f"Last BMI is {bmi_info['value']} " if bmi_info else ''
        spo2_str = f"Last SPO2 is {spo2_info['value']} " if spo2_info else ''
        temperature_str = f"Last Temperature is {temperature_info['value']} Fahrenheit" if temperature_info else ''

        vitals_str = height_str + weight_str + pulse_rate_str + bmi_str + spo2_str + temperature_str
        
        generate_summary_100_words(original_patient_data['data'])
        generate_summary_200_words(original_patient_data['data'], vitals_str)
        generate_summary_500_words(original_patient_data['data'], vitals_str)

        
if __name__ == "__main__":
    main()
