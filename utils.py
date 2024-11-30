import xml.etree.ElementTree as ET
from datetime import date

def generate_pain_xml(msg_id=None, 
                      creation_time=str(date.today()),
                      num_transactions="2", 
                      debtor_accounts=None, 
                      creditor_accounts=None, 
                      amount_type=None, 
                      currency="EUR", 
                      fixed_amount=None, 
                      min_amount=None, 
                      max_amount=None, 
                      is_unstructured=True,
                      initiating_party_name="initiatingParty",
                      initiating_party_org_bic="BICcode",
                      initiating_party_org_lei="LEIcode",
                      payment_inf_id="paymentInfId",
                      execution_date=str(date.today()),
                      debtor_name="debtorName",
                      debtor_department="debtorDepartment",
                      debtor_sub_department="debtorSubDepartment",
                      debtor_street_name="debtorStreetName",
                      debtor_building_number="debtorBuildingNumber",
                      debtor_floor="debtorFloor",
                      debtor_post_box="debtorPostBox",
                      debtor_room="debtorRoom",
                      debtor_postal_code="debtorPostalCode",
                      debtor_town_name="debtorTownName",
                      debtor_district_name="debtorDistrictName",
                      debtor_country_subdivision="debtorCountrySubDivision",
                      debtor_country="debtorCountry",
                      debtor_org_bic="BICcode",
                      debtor_org_lei="LEIcode",
                      debtor_agent_bic="BICcode",
                      cdtr_instr_id="creditorInstructionId",
                      end_to_end_id="endToEndId",
                      creditor_name="creditorName",
                      creditor_street_name="creditorStreetName",
                      creditor_building_number="creditorBuildingNumber",
                      creditor_floor="creditorFloor",
                      creditor_postal_code="creditorPostalCode",
                      creditor_town_name="creditorTownName",
                      creditor_country="creditorCountry",
                      creditor_org_bic="BICcode",
                      creditor_org_lei="LEIcode",
                      unstructured_remittance_text="unstructuredRemittanceInformation",
                      structured_remittance_type="SCOR",
                      structured_remittance_ref="StructuredReference",
                      is_consolidated=False,
                      category_purpose="SALA",
                      number_of_creditor_blocks="1"):
    # Create root element
    root = ET.Element("Document", xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.09")
    ccti = ET.SubElement(root, "CstmrCdtTrfInitn")

    # Header block
    grp_hdr = ET.SubElement(ccti, "GrpHdr")
    ET.SubElement(grp_hdr, "MsgId").text = msg_id
    ET.SubElement(grp_hdr, "CreDtTm").text = creation_time

    # Total number of transactions. Calculating number of "CdtTrfTxInf" blocks.
    if is_consolidated:
        ET.SubElement(grp_hdr, "NbOfTxs").text = str(number_of_creditor_blocks)
    else:
        ET.SubElement(grp_hdr, "NbOfTxs").text = str(num_transactions)

    ET.SubElement(grp_hdr, "CtrlSum").text = "0.00"  # Placeholder
    initg_pty = ET.SubElement(grp_hdr, "InitgPty")
    ET.SubElement(initg_pty, "Nm").text = initiating_party_name
    org_id = ET.SubElement(initg_pty, "OrgId")
    ET.SubElement(org_id, "AnyBIC").text = initiating_party_org_bic
    ET.SubElement(org_id, "LEI").text = initiating_party_org_lei

    # Payment information block
    debtor_list = debtor_accounts.split(",")
    creditor_list = creditor_accounts.split(",")
    total_sum = 0.0
    ctrl_sum = 0.0

    # Find number of payment and creditor block instances
    if is_consolidated:
        num_transactions = 1
    else:
        number_of_creditor_blocks = 1

    for i in range(num_transactions):

        # Null payment sum
        ctrl_sum = 0.0
        
        # Add new payment block
        pmt_inf = ET.SubElement(ccti, "PmtInf")
        ET.SubElement(pmt_inf, "PmtInfId").text = payment_inf_id + "_" + str(i+1)
        ET.SubElement(pmt_inf, "PmtMtd").text = "TRF"
        ET.SubElement(pmt_inf, "BtchBookg").text = "false"
        ET.SubElement(pmt_inf, "NbOfTxs").text = str(number_of_creditor_blocks)
        
        # Update CtrlSum for this PmtInf
        ET.SubElement(pmt_inf, "CtrlSum").text = "0.00" # Placeholder

        # Check if payment is consolidated
        if is_consolidated:
            pmt_tp_inf = ET.SubElement(pmt_inf, "PmtTpInf")
            svc_lvl = ET.SubElement(pmt_tp_inf, "SvcLvl")
            ET.SubElement(svc_lvl, "Cd").text = "SEPA"
            cgty_purpose = ET.SubElement(pmt_tp_inf, "CtgyPurp")
            ET.SubElement(cgty_purpose, "Cd").text = category_purpose

        # Request Execution Date
        reqd_exctn_dt = ET.SubElement(pmt_inf, "ReqdExctnDt")
        ET.SubElement(reqd_exctn_dt, "Dt").text = execution_date

        # Debtor Info
        dbtr = ET.SubElement(pmt_inf, "Dbtr")
        ET.SubElement(dbtr, "Nm").text = debtor_name
        pstl_addr = ET.SubElement(dbtr, "PstlAdr")
        ET.SubElement(pstl_addr, "Dept").text = debtor_department
        ET.SubElement(pstl_addr, "SubDept").text = debtor_sub_department
        ET.SubElement(pstl_addr, "StrtNm").text = debtor_street_name
        ET.SubElement(pstl_addr, "BldgNb").text = debtor_building_number
        ET.SubElement(pstl_addr, "Flr").text = debtor_floor
        ET.SubElement(pstl_addr, "PstBx").text = debtor_post_box
        ET.SubElement(pstl_addr, "Room").text = debtor_room
        ET.SubElement(pstl_addr, "PstCd").text = debtor_postal_code
        ET.SubElement(pstl_addr, "TwnNm").text = debtor_town_name
        ET.SubElement(pstl_addr, "DstrctNm").text = debtor_district_name
        ET.SubElement(pstl_addr, "CtrySubDvsn").text = debtor_country_subdivision
        ET.SubElement(pstl_addr, "Ctry").text = debtor_country
        org_id = ET.SubElement(dbtr, "OrgId")
        ET.SubElement(org_id, "AnyBIC").text = debtor_org_bic
        ET.SubElement(org_id, "LEI").text = debtor_org_lei

        # Debtor Account
        dbtr_acct = ET.SubElement(pmt_inf, "DbtrAcct")
        dbtr_id = ET.SubElement(dbtr_acct, "Id")

        # Check if payment is consolidated. If "Yes" - take the first debtor account from the list
        if is_consolidated:
            ET.SubElement(dbtr_id, "IBAN").text = debtor_list[0]
        else:
            ET.SubElement(dbtr_id, "IBAN").text = debtor_list[i % len(debtor_list)]
        ET.SubElement(dbtr_acct, "Ccy").text = currency

        # Debtor Agent
        dbtr_agt = ET.SubElement(pmt_inf, "DbtrAgt")
        fin_instn_id = ET.SubElement(dbtr_agt, "FinInstnId")
        ET.SubElement(fin_instn_id, "BICFI").text = debtor_agent_bic

        for j in range(number_of_creditor_blocks):
            # Creditor
            cdt_trf_tx_inf = ET.SubElement(pmt_inf, "CdtTrfTxInf")

            # Payment Identification
            pmt_id = ET.SubElement(cdt_trf_tx_inf, "PmtId")
            ET.SubElement(pmt_id, "InstrId").text = cdtr_instr_id + "_" + str(j+1)
            ET.SubElement(pmt_id, "EndToEndId").text = end_to_end_id

            # Add Amount to Creditor Info
            amt = ET.SubElement(cdt_trf_tx_inf, "Amt")

            # Calculate amount for this payment
            if amount_type == "Fixed Amount":
                amount = float(fixed_amount)
            else:
                import random
                amount = random.uniform(min_amount, max_amount)
            ctrl_sum += amount

            ET.SubElement(amt, "InstdAmt", Ccy=currency).text = f"{amount:.2f}"

            # Creditor Info
            cdtr = ET.SubElement(cdt_trf_tx_inf, "Cdtr")
            ET.SubElement(cdtr, "Nm").text = creditor_name
            pstl_addr = ET.SubElement(cdtr, "PstlAdr")
            ET.SubElement(pstl_addr, "StrtNm").text = creditor_street_name
            ET.SubElement(pstl_addr, "BldgNb").text = creditor_building_number
            ET.SubElement(pstl_addr, "Flr").text = creditor_floor
            ET.SubElement(pstl_addr, "PstCd").text = creditor_postal_code
            ET.SubElement(pstl_addr, "TwnNm").text = creditor_town_name
            ET.SubElement(pstl_addr, "Ctry").text = creditor_country
            org_id = ET.SubElement(cdtr, "OrgId")
            ET.SubElement(org_id, "AnyBIC").text = creditor_org_bic
            ET.SubElement(org_id, "LEI").text = creditor_org_lei

            # Creditor Account
            cdtr_acct = ET.SubElement(cdt_trf_tx_inf, "CdtrAcct")
            cdtr_id = ET.SubElement(cdtr_acct, "Id")
            ET.SubElement(cdtr_id, "IBAN").text = creditor_list[i % len(creditor_list)]

            # Remittance Information
            if is_unstructured:
                rmt_inf = ET.SubElement(cdt_trf_tx_inf, "RmtInf")
                ET.SubElement(rmt_inf, "Ustrd").text = unstructured_remittance_text
            else:
                rmt_inf = ET.SubElement(cdt_trf_tx_inf, "RmtInf")
                strd = ET.SubElement(rmt_inf, "Strd")
                cdtr_ref_inf = ET.SubElement(strd, "CdtrRefInf")
                type = ET.SubElement(cdtr_ref_inf, "Tp")
                cd_or_prtry = ET.SubElement(type, "CdOrPrtry")
                ET.SubElement(cd_or_prtry, "Cd").text = structured_remittance_type
                ET.SubElement(cdtr_ref_inf, "Ref").text = structured_remittance_ref

        # Add amount to payment block
        pmt_inf.find("CtrlSum").text = f"{ctrl_sum:.2f}"

        # Add payment amount to total amount
        total_sum += ctrl_sum

    # Update CtrlSum
    grp_hdr.find("CtrlSum").text = f"{total_sum:.2f}"

    # Write to file
    tree = ET.ElementTree(root)
    tree.write("generated_pain.xml", encoding="utf-8", xml_declaration=True)

def download_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()