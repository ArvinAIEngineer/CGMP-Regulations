import streamlit as st
import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Gemini API key from .env file
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)

# Long context to be used for all queries
LONG_CONTEXT = """
On March 30, 2025, 21 CFR Part 211, titled Current Good Manufacturing Practice for Finished Pharmaceuticals, under Title 21, Chapter I, Subchapter C of the Code of Federal Regulations, administered by the Food and Drug Administration (FDA), Department of Health and Human Services, sets forth minimum standards for preparation of drug products (excluding positron emission tomography drugs) for administration to humans or animals, with authority from 21 U.S.C. 321, 351, 352, 355, 360b, 371, 374 and 42 U.S.C. 216, 262, 263a, 264, published at 43 FR 45077 on September 29, 1978, and amended at 89 FR 51769 on June 18, 2024, among others; Subpart A—General Provisions includes §211.1 Scope stating regulations contain minimum CGMP for drug products, supplemented by Parts 600-680 for biological products and Part 1271 for human cells, tissues, and cellular/tissue-based products unless explicitly superseded, with §211.1(b) noting CGMP in this chapter pertains to drugs and biologics, and §211.1(c) exempting OTC drug products marketed as foods from enforcement pending a proposed exemption in the Federal Register of September 29, 1978, applying Parts 110-129 instead, and §211.3 Definitions referencing definitions in §210.3; Subpart B—Organization and Personnel includes §211.22 Responsibilities of quality control unit requiring a unit with responsibility and authority to approve or reject components, drug product containers, closures, in-process materials, packaging material, labeling, and drug products, including those manufactured by contract, with adequate lab facilities, written procedures for approving procedures/specifications impacting identity, strength, quality, and purity, §211.25 Personnel qualifications mandating education, training, and experience for personnel in manufacturing, processing, packing, or holding, with CGMP training by qualified individuals on a continuing basis, supervisors similarly qualified, and adequate staffing, §211.28 Personnel responsibilities requiring clean clothing, protective apparel (head, face, hand, arm coverings) as needed, good sanitation/health habits, restricted access to authorized personnel only, exclusion of personnel with illness or open lesions from direct contact until corrected, with reporting of adverse health conditions, and §211.34 Consultants requiring sufficient education, training, experience, with records of name, address, qualifications, and service type; Subpart C—Buildings and Facilities includes §211.42 Design and construction features requiring suitable size, construction, location for cleaning, maintenance, and operations, adequate space to prevent mix-ups and contamination, separate/defined areas for receipt, storage, holding rejected items, in-process materials, manufacturing, packaging, quarantine, released drug storage, lab operations, and aseptic processing with smooth surfaces, temperature/humidity controls, HEPA-filtered air under positive pressure, monitoring systems, cleaning/disinfection systems, and separate penicillin facilities, §211.44 Lighting requiring adequate lighting in all areas, §211.46 Ventilation, air filtration, air heating and cooling requiring adequate ventilation, control over air pressure, microorganisms, dust, humidity, temperature, air filtration with prefilters and particulate filters, measures to control dust recirculation, exhaust systems for contamination areas, and separate air-handling for penicillin, §211.48 Plumbing requiring potable water under continuous positive pressure meeting EPA standards in 40 CFR Part 141, no defective systems, drains with air breaks to prevent back-siphonage, §211.50 Sewage and refuse requiring safe, sanitary disposal of sewage, trash, and refuse, §211.52 Washing and toilet facilities requiring hot/cold water, soap/detergent, air driers or single-service towels, clean toilets near work areas, §211.56 Sanitation requiring clean, sanitary buildings free of rodents, birds, insects, vermin (except lab animals), with written procedures for cleaning schedules, methods, equipment, materials, use of registered rodenticides/insecticides per 7 U.S.C. 135, applying to contractors and employees, and §211.58 Maintenance requiring buildings in good repair; Subpart D—Equipment includes §211.63 Equipment design, size, and location requiring appropriate design, adequate size, suitable location for use, cleaning, and maintenance, §211.65 Equipment construction requiring non-reactive, non-additive, non-absorptive surfaces, no contact with lubricants/coolants altering safety, identity, strength, quality, purity, §211.67 Equipment cleaning and maintenance requiring cleaning, maintenance, sanitization/sterilization at intervals to prevent contamination, with written procedures for responsibility, schedules, methods, equipment disassembly/reassembly, removal of prior batch ID, protection of clean equipment, pre-use inspection, records per §211.180 and §211.182, §211.68 Automatic, mechanical, and electronic equipment allowing use if calibrated, inspected, checked per written program, with records, secure controls over computer systems, verified input/output, backups (hard copy, tapes, microfilm) except for certain lab calculations, and one-person operation with equipment checks per §§211.101, 211.103, 211.182, 211.188, and §211.72 Filters prohibiting asbestos filters in injectables, requiring non-fiber-releasing filters with 0.2-micron (or 0.45-micron if dictated) pore size if fiber-releasing filters are used; Subpart E—Control of Components and Drug Product Containers and Closures includes §211.80 General requirements requiring written procedures for receipt, identification, storage, handling, sampling, testing, approval/rejection, off-floor storage, lot coding, quarantine/approved/rejected status, §211.82 Receipt and storage requiring visual exam for labeling, damage, contamination, quarantine until tested per §211.80, §211.84 Testing and approval or rejection requiring sampling, testing, or examination before use, representative sampling based on statistical criteria, supplier analysis with manufacturer identity test and validation, testing for identity, purity, strength, quality, filth, microbial contamination, with rejection if specs not met, §211.86 Use requiring oldest approved stock first unless deviation is temporary/appropriate, §211.87 Retesting requiring retesting per §211.84 after long storage or adverse conditions, §211.89 Rejected components requiring quarantine to prevent use, and §211.94 Drug product containers and closures requiring non-reactive, protective, clean, sterilized/depyrogenated containers/closures, validated processes, gas-specific outlet connections for portable cryogenic medical gas containers, durable labeling per §201.328; Subpart F—Production and Process Controls includes §211.100 Written procedures; deviations requiring written procedures drafted, reviewed, approved by organizational units and QCU, documented deviations justified, §211.101 Charge-in of components requiring formulation with ≥100% active ingredient, weighed/measured components identified by name, code, number, weight, batch, verified by two persons or one with automated equipment per §211.68, §211.103 Calculation of yield requiring actual/theoretical yield at each phase, verified by two persons or one with automated equipment, §211.105 Equipment identification requiring labeled containers, lines, equipment with contents and processing phase, distinctive equipment ID in batch records, §211.110 Sampling and testing requiring written in-process control procedures for tablet weight, disintegration, mixing, dissolution, clarity, pH, bioburden, with valid specs, testing for identity, strength, quality, purity, quarantine of rejected materials, §211.111 Time limitations requiring time limits for production phases, deviations justified if quality unaffected, §211.113 Control of microbiological contamination requiring procedures to prevent objectionable microbes in non-sterile products and validate aseptic/sterilization processes for sterile products, and §211.115 Reprocessing requiring written reprocessing procedures approved by QCU; Subpart G—Packaging and Labeling Control includes §211.122 Materials examination and usage criteria requiring written procedures for receipt, storage, sampling, testing of labeling/packaging, separate storage, destruction of obsolete materials, special controls for cut/gang-printed labeling, §211.125 Labeling issuance requiring strict control, examination for conformity, reconciliation of quantities issued/used/returned unless 100% examined per §211.122(g)(2), destruction of excess lot-numbered labeling, secure storage, §211.130 Packaging and labeling operations requiring written procedures to prevent mix-ups, identification of unlabeled containers, lot/control numbers, pre-use inspection of facilities, §211.132 Tamper-evident packaging for OTC drugs requiring tamper-evident packages with visible indicators for OTC drugs (except dermatological, dentifrice, insulin, lozenge), sealed two-piece capsules, labeling identifying features, exemptions via petition per §10.30, §211.134 Drug product inspection requiring examination during finishing, representative sampling post-finishing, recorded results, and §211.137 Expiration dating requiring dates from stability testing per §211.166, related to storage conditions, with exemptions for homeopathic drugs, allergenic extracts, investigational drugs; Subpart H—Holding and Distribution includes §211.142 Warehousing procedures requiring quarantine and storage under appropriate temperature, humidity, light conditions, and §211.150 Distribution procedures requiring oldest stock distributed first unless deviation is temporary/appropriate, with lot traceability for recalls; Subpart I—Laboratory Controls includes §211.160 General requirements requiring written specs, standards, sampling plans, test procedures approved by QCU, deviations recorded/justified, scientifically sound controls, calibration per written program, §211.165 Testing and release requiring lab testing for conformance to specs (identity, strength, microbes) before release, validated test methods, rejection/reprocessing if specs not met, §211.166 Stability testing requiring written programs with sample sizes, test intervals, storage conditions, reliable methods, testing in marketed container-closure systems, accelerated studies for tentative dates, exemptions for homeopathic drugs/allergenic extracts, §211.167 Special testing requiring sterility/pyrogen tests, foreign particle tests for ophthalmic ointments, release rate tests for controlled-release forms, §211.170 Reserve samples requiring retention of twice the quantity needed for tests (except sterility/pyrogens) for one year post-expiration, three months/six months for radioactive drugs, three years for exempt OTC drugs, annual visual exams, no retention for compressed medical gases, §211.173 Laboratory animals requiring maintenance/control for suitability, with use history records, and §211.176 Penicillin contamination requiring testing per FDA procedures if cross-contamination is possible; Subpart J—Records and Reports includes §211.180 General requirements requiring batch records retained for one year post-expiration (three years for exempt OTC drugs), component records for one year post-expiration, availability for FDA inspection, annual quality evaluations, notification of responsible officials of investigations/recalls, §211.182 Equipment cleaning and use log requiring records of cleaning, maintenance, use with date, time, product, lot, signed by performers/checkers, §211.184 Component records requiring identity, quantity, supplier, lot numbers, test results, inventory, disposition, §211.186 Master production and control records requiring signed records with product name, strength, dosage, ingredients, weights, yield, container specs, manufacturing instructions, §211.188 Batch production and control records requiring reproduction of master records, documentation of steps (dates, equipment, components, yields, labeling, sampling), §211.192 Production record review requiring QCU review for compliance, investigation of discrepancies extending to associated batches, §211.194 Laboratory records requiring complete test data (sample details, methods, results, calibration, stability), §211.196 Distribution records requiring product name, strength, consignee, date, quantity, lot number (except compressed medical gases), and §211.198 Complaint files requiring written procedures, records of complaints (name, strength, lot, complainant, nature, reply), investigations per §211.192; Subpart K—Returned and Salvaged Drug Products includes §211.204 Returned drug products requiring identification, holding, destruction unless proven safe via testing, investigation of associated batches, and §211.208 Drug product salvaging prohibiting salvaging unless lab tests and premise inspections confirm standards after improper storage; simultaneously, the Perficient Ultimate Guide to 21 CFR Part 11 details regulations under Title 21, Chapter I, Subchapter A, Part 11, addressing electronic records and signatures, with Subpart A—General Provisions including §11.1 Scope stating criteria for trustworthy, reliable electronic records, signatures, and handwritten signatures on electronic records as equivalent to paper records and handwritten signatures, applying to records created, modified, maintained, archived, retrieved, or transmitted under FDA regulations, including submissions under the Federal Food, Drug, and Cosmetic Act and Public Health Service Act, excluding paper records transmitted electronically, with electronic signatures equivalent to handwritten unless excepted post-August 20, 1997, electronic records usable in lieu of paper per §11.2 unless paper required, systems subject to FDA inspection, excluding records under §§1.326-1.368, §11.2 Implementation allowing electronic records/signatures for non-submitted records if Part 11-compliant, for submitted records if compliant and listed in docket 92S-0251, specifying acceptable document types and receiving units, requiring paper if not listed, with consultation advised, and §11.3 Definitions defining Act as Federal Food, Drug, and Cosmetic Act (21 U.S.C. 321-393), Agency as FDA, Biometrics as identity verification via physical features or actions, Closed system as access controlled by record custodians, Digital signature as cryptographic authentication, Electronic record as digital text, graphics, data, audio, pictorial info, Electronic signature as legally binding symbol compilation, Handwritten signature as scripted name/mark, Open system as access not controlled by record custodians; Subpart B—Electronic Records includes §11.10 Controls for closed systems requiring procedures/controls for authenticity, integrity, confidentiality, irrefutability, with validation for accuracy/reliability, human-readable/electronic copies for FDA, record protection for retention period, access limited to authorized individuals, secure, time-stamped audit trails recording entries/actions, operational checks for sequencing, authority checks for access/signing, device checks for data validity, qualified personnel, accountability policies, controls over system documentation (distribution, revision, audit trails), §11.30 Controls for open systems requiring all §11.10 controls plus encryption, digital signature standards for authenticity, integrity, confidentiality, §11.50 Signature manifestations requiring signed records to show printed name, date, time, meaning (review, approval, responsibility, authorship), subject to same controls, included in human-readable forms, and §11.70 Signature/record linking requiring electronic/handwritten signatures linked to records to prevent excision, copying, falsification; Subpart C—Electronic Signatures includes §11.100 General requirements mandating unique signatures not reused/reassigned, identity verification before use, certification to FDA that signatures post-August 20, 1997, are legally binding, submitted in paper with handwritten signature to Office of Regional Operations (HFC-100), 5600 Fishers Lane, Rockville, MD 20857, with additional certification if requested, §11.200 Electronic signature components and controls requiring non-biometric signatures to use two components (ID/password), first signing in session using all components, subsequent signings using one, all components per signing if not continuous, exclusive to owners, requiring collaboration for others’ use, biometric signatures exclusive to owners, and §11.300 Controls for identification codes/passwords requiring unique ID/password combos, periodic checks/recalls/revisions, loss management for tokens/devices, safeguards against unauthorized use with immediate reporting, initial/periodic testing of devices for function/authenticity.

"""

def generate_response(query, history=None):
    model = "gemini-2.0-flash"
    
    # Create chat instance if history is provided
    if history:
        chat = client.chats.create(model=model)
        
        # Recreate chat history
        for message in history:
            if message["role"] == "user":
                chat.send_message(message["content"])
            # Skip assistant messages as they'll be generated when we send user messages
        
        # Stream the response to the latest message
        response_stream = chat.send_message_stream(query)
        full_response = ""
        
        for chunk in response_stream:
            chunk_text = chunk.text
            full_response += chunk_text
            yield chunk_text
            
        # Return the complete chat history including the new response
        updated_history = history.copy()
        updated_history.append({"role": "user", "content": query})
        updated_history.append({"role": "assistant", "content": full_response})
        return full_response, updated_history
    
    else:
        # For first-time queries with no history, use the system instruction and context
        system_instruction = f"""You are a helpful pharmaceutical regulation assistant specializing in 
        You are a helpful pharma regulation assistant specializing in 21 CFR Part 211 and Part 11. Use conversational language while maintaining 
        technical accuracy. Base your answers on the following context:
        
        {LONG_CONTEXT}
        
        If you're unsure about something or if it's not covered in the context, acknowledge it rather than 
        providing potentially incorrect information."""
        
        generate_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,  # Lower temperature for more factual responses
            max_output_tokens=8000,  # Allow for comprehensive answers
        )
        
        contents = [query]
        
        # Stream response
        full_response = ""
        
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_config,
        ):
            chunk_text = chunk.text
            full_response += chunk_text
            yield chunk_text
            
        # Create history for future use
        new_history = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": full_response}
        ]
        
        return full_response, new_history

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app layout
st.title("Pharmaceutical Regulation Assistant")
st.write("Ask questions about 21 CFR Part 211 and Part 11.")

# Display chat history
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").write(content)

# User input using chat_input instead of text_input for better UX
user_query = st.chat_input("Ask a question about pharmaceutical regulations...")

if user_query:
    # Add user message to chat display
    st.chat_message("user").write(user_query)
    
    # Display assistant response with streaming
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream in the response
        response_container = st.container()
        
        if len(st.session_state.chat_history) > 0:
            # Use chat history for context
            response_generator = generate_response(user_query, st.session_state.chat_history)
        else:
            # First message
            response_generator = generate_response(user_query)
        
        for chunk in response_generator:
            if isinstance(chunk, tuple):
                # This is the final return value with the full response and history
                full_response, st.session_state.chat_history = chunk
                break
            else:
                # This is a text chunk
                full_response += chunk
                response_placeholder.write(full_response)
                
        # Ensure the final response is displayed
        response_placeholder.write(full_response)

# Add a clear conversation button
if st.button("Clear Conversation"):
    st.session_state.chat_history = []
    st.rerun()

if __name__ == "__main__":
    pass
