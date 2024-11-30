import streamlit as st
from utils import generate_pain_xml, download_file
from datetime import date

st.title("Pain XML Generator")
st.write("This is a Streamlit app that generates pain XML files. It's purpose is to allow large pain files generation with a substantial amount of payment instances.")
st.write("Supported pain version: _pain.001.001.09_")
st.divider()

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

# Basic Inputs Section
with st.expander("Basic Inputs", expanded=False):
    st.header("Basic Inputs")

    # Header inputs
    msg_id = st.text_input("Message ID (MsgId)", value="messageIdentification", max_chars=35)
    creation_time = st.text_input("Creation Date Time (CreDtTm)", value=str(date.today()), max_chars=10)
    num_transactions = st.number_input("Number of Separate Payments (PmtInf)", min_value=1, max_value=1000000, step=1)

    # Account inputs
    st.write("If consolidated payment is selected, only one debtor account is allowed (first account from the list will be taken).")
    debtor_accounts = st.text_area("Debtor Accounts (comma-separated)", 
        "LT444010000100561111,LT444010000100562222,LT444010000100563333")
    creditor_accounts = st.text_area("Creditor Accounts (comma-separated)", 
        "LT587400000013547777,LT587400000013548888,LT587400000013549999")

    # Amount and currency inputs
    amount_type = st.radio(
        "Select Amount Type",
        options=["Fixed Amount", "Randomized Amount Between Min and Max"],
        index=0
    )

    if amount_type == "Fixed Amount":
        fixed_amount = st.number_input("Fixed Amount (e.g., 1.00)", min_value=0.01, format="%.2f")
    else:
        min_amount = st.number_input("Minimum Amount", min_value=0.0, step=1.0, format="%.2f")
        max_amount = st.number_input("Maximum Amount", min_value=min_amount+0.01, step=1.0, format="%.2f")

    currency = st.text_input("Currency", value="EUR", max_chars=3)

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

st.divider()

# Advanced Inputs Section
with st.expander("Advanced Inputs", expanded=False):
    st.header("Advanced Inputs")
    # Consolidated Payment
    select_consolidated = st.radio(
        "Select Consolidated Payment",
        options=["No", "Yes"],
        index=0
    )

    is_consolidated = False

    if select_consolidated == "Yes":
        is_consolidated = True
    else:
        is_consolidated = False

    category_purpose = None
    number_of_creditor_blocks = 1

    if is_consolidated:
        category_purpose = st.text_input("Category Purpose (CtgyPurp)", "SALA")
        number_of_creditor_blocks = st.number_input("Number of Transaction Blocks (CdtTrfTxInf)", min_value=1, max_value=1000000, step=1)

    # Initiating Party
    initiating_party_name = st.text_input("Initiating Party (InitgPty/Nm)", "initiatingParty")
    initiating_party_org_bic = st.text_input("Initiating Party Organization BIC (InitgPty/OrgId/AnyBIC)", "BICcode")
    initiating_party_org_lei = st.text_input("Initiating Party Organization LEI (InitgPty/OrgId/LEI)", "LEIcode")

    # Payment Information Id
    st.write("Base part of payment information identification. Package payments will be numbered like so: base + _1, i.e. paymentInfId_1, paymentInfId_2, etc.")
    payment_inf_id = st.text_input("Payment Information ID (PmtInfId)", "paymentInfId")

    # Execution date
    st.write("Execution date of the payment. Default value is today's date.")
    execution_date = st.text_input("Execution Date (ReqdExctnDt/Dt)", value=str(date.today()))

    st.divider()

    # Debtor Information
    st.write("Debtor Information Inputs")

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        debtor_name = st.text_input("Debtor Name (Dbtr/Nm)", "debtorName")
        debtor_department = st.text_input("Debtor Department (Dbtr/PstlAdr/Dept)", "debtorDepartment")
        debtor_sub_department = st.text_input("Debtor Sub-Department (Dbtr/PstlAdr/SubDept)", "debtorSubDepartment")
        debtor_street_name = st.text_input("Debtor Street Name (Dbtr/PstlAdr/StrtNm)", "debtorStreetName")
        debtor_building_number = st.text_input("Debtor Building Number (Dbtr/PstlAdr/BldgNb)", "debtorBuildingNumber")
        debtor_floor = st.text_input("Debtor Floor (Dbtr/PstlAdr/Flr)", "debtorFloor")
        debtor_post_box = st.text_input("Debtor Post Box (Dbtr/PstlAdr/PstBx)", "debtorPostBox")

    with col2:
        debtor_postal_code = st.text_input("Debtor Postal Code (Dbtr/PstlAdr/PstCd)", "debtorPostalCode")
        debtor_town_name = st.text_input("Debtor Town Name (Dbtr/PstlAdr/TwnNm)", "debtorTownName")
        debtor_country_subdivision = st.text_input("Debtor Country Subdivision (Dbtr/PstlAdr/CtrySubDvsn)", "debtorCountrySubdivision")
        debtor_country = st.text_input("Debtor Country (Dbtr/PstlAdr/Ctry)", "debtorCountry")

        debtor_org_bic = st.text_input("Debtor Organization BIC (Dbtr/OrgId/AnyBIC)", "BICcode")
        debtor_org_lei = st.text_input("Debtor Organization LEI (Dbtr/OrgId/LEI)", "LEIcode")

        # Debtor Agent
        debtor_agent_bic = st.text_input("Debtor Agent BIC (DbtrAgt/FinInstnId/BICFI)", "BICcode")
    
    st.divider()

    # Creditor Information Identification
    st.write("Base part of creditor information identification. Package payments will be numbered like so: base + _1, i.e. creditorInstructionId_1, creditorInstructionId_2, etc.")
    cdtr_instr_id = st.text_input("Creditor Instruction ID (CdtTrfTxInf/PmtId/InstrId)", "creditorInstructionId")
    end_to_end_id = st.text_input("End-to-End ID (CdtTrfTxInf/PmtId/EndToEndId)", "endToEndId")

    st.divider()

    # Creditor Information
    st.write("Creditor Information Inputs")

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        creditor_name = st.text_input("Creditor Name (Cdtr/Nm)", "creditorName")
        creditor_street_name = st.text_input("Creditor Street Name (Cdtr/PstlAdr/StrtNm)", "creditorStreetName")
        creditor_building_number = st.text_input("Creditor Building Number (Cdtr/PstlAdr/BldgNb)", "creditorBuildingNumber")
        creditor_floor = st.text_input("Creditor Floor (Cdtr/PstlAdr/Flr)", "creditorFloor")
        creditor_postal_code = st.text_input("Creditor Postal Code (Cdtr/PstlAdr/PstCd)", "creditorPostalCode")

    with col2:
        creditor_town_name = st.text_input("Creditor Town Name (Cdtr/PstlAdr/TwnNm)", "creditorTownName")
        creditor_country = st.text_input("Creditor Country (Cdtr/PstlAdr/Ctry)", "creditorCountry")

        creditor_org_bic = st.text_input("Creditor Organization BIC (Cdtr/OrgId/AnyBIC)", "BICcode")
        creditor_org_lei = st.text_input("Creditor Organization LEI (Cdtr/OrgId/LEI)", "LEIcode")

    st.divider()
    
    # Remittance Information
    st.write("Remittance Information Inputs")
    remittance_info_type = st.radio(
        "Select Remittance Information Type",
        options=["Unstructured", "Structured"],
        index=0
    )

    unstructured_remittance_text = None
    structured_remittance_type = None
    structured_remittance_ref = None

    if remittance_info_type == "Unstructured":
        unstructured_remittance = True
        unstructured_remittance_text = st.text_input("Unstructured Remittance Information", "unstructuredRemittanceInformation")
    else:
        unstructured_remittance = False
        structured_remittance_type = st.text_input("Structured Remittance Type", "SCOR")
        structured_remittance_ref = st.text_input("Structured Remittance Reference", "StructuredReference")

#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------

st.divider()

# Download Section
st.header("Generate & Download")

# Generate Button
if st.button("Generate"):
    generate_pain_xml(
        msg_id=msg_id,
        creation_time=creation_time,
        num_transactions=num_transactions,
        debtor_accounts=debtor_accounts,
        creditor_accounts=creditor_accounts,
        amount_type=amount_type,
        currency=currency,
        fixed_amount=fixed_amount if amount_type == "Fixed Amount" else None,
        min_amount=min_amount if amount_type == "Randomized Amount Between Min and Max" else None,
        max_amount=max_amount if amount_type == "Randomized Amount Between Min and Max" else None,
        is_unstructured=unstructured_remittance,
        initiating_party_name=initiating_party_name,
        initiating_party_org_bic=initiating_party_org_bic,
        initiating_party_org_lei=initiating_party_org_lei,
        payment_inf_id=payment_inf_id,
        execution_date=execution_date,
        debtor_name=debtor_name,
        debtor_department=debtor_department,
        debtor_sub_department=debtor_sub_department,
        debtor_street_name=debtor_street_name,
        debtor_building_number=debtor_building_number,
        debtor_floor=debtor_floor,
        debtor_post_box=debtor_post_box,
        debtor_postal_code=debtor_postal_code,
        debtor_town_name=debtor_town_name,
        debtor_country_subdivision=debtor_country_subdivision,
        debtor_country=debtor_country,
        debtor_org_bic=debtor_org_bic,
        debtor_org_lei=debtor_org_lei,
        debtor_agent_bic=debtor_agent_bic,
        cdtr_instr_id=cdtr_instr_id,
        end_to_end_id=end_to_end_id,
        creditor_name=creditor_name,
        creditor_street_name=creditor_street_name,
        creditor_building_number=creditor_building_number,
        creditor_floor=creditor_floor,
        creditor_postal_code=creditor_postal_code,
        creditor_town_name=creditor_town_name,
        creditor_country=creditor_country,
        creditor_org_bic=creditor_org_bic,
        creditor_org_lei=creditor_org_lei,
        unstructured_remittance_text=unstructured_remittance_text,
        structured_remittance_type=structured_remittance_type,
        structured_remittance_ref=structured_remittance_ref,
        is_consolidated=is_consolidated,
        category_purpose=category_purpose,
        number_of_creditor_blocks=number_of_creditor_blocks
    )
    st.success("XML file generated successfully!")

# Download Button
st.download_button("Download XML", download_file("generated_pain.xml"), file_name="generated_pain.xml")