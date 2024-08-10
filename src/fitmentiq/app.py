import streamlit as st
from fitmentiq.crew import FitmentiqCrew
import tempfile
from fitmentiq.gmail_agent import GmailAgent
import os
import yaml
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
load_dotenv(".env")



class FitmentiqGenUI:


    def parse_data(self, file_path:str):
        loader = PyPDFLoader(file_path)
        data = loader.load()
        all_content = ""
        for page in data:
            all_content += page.page_content + "\n"

        if all_content == "":
            raise ValueError("Nothing to extract in Pdf")
        
        return all_content
    
    def generate_fitmentiq(self):

        with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to temporary directory
            jd_path = os.path.join(temp_dir, "job_description.pdf")
            with open(jd_path, "wb") as f:
                f.write(st.session_state.job_description)
                
            if st.session_state.index < st.session_state.total_no_resumes:
            # Save current resume to temporary directory
                resume_path = os.path.join(temp_dir, f"resume_{st.session_state.index}.pdf")
                with open(resume_path, "wb") as f:
                    f.write(st.session_state.resumes[st.session_state.index])
                st.session_state.index += 1
                st.header(f"## Candidate: {st.session_state.index}")
                st.session_state.jd_data = self.parse_data(jd_path)
                with st.chat_message("AI"):
                    st.write(f"Agent Name: JD_parser")
                    st.write(st.session_state.jd_data)
                    st.session_state.previous_results.append({"Agent_Name":"JD_parser", "output":st.session_state.jd_data})
                st.session_state.resume_data = self.parse_data(resume_path)
                with st.chat_message("AI"):
                    st.write(f"Agent Name: Resume_parser")
                    st.write(st.session_state.resume_data)
                    st.session_state.previous_results.append({"Agent_Name":"Resume_parser", "output":st.session_state.resume_data})
                dataset = {"job_description": st.session_state.jd_data, "resumes": st.session_state.resume_data}
                st.session_state.result = FitmentiqCrew().crew().kickoff(inputs=dataset)
                print(st.session_state.result)
                st.session_state.generating = False
                st.rerun()
            else:
                st.title("FitmentIQ generated successfully!")
                st.header(f"No of Resumes Reviwed - {st.session_state.total_no_resumes}")
                st.header(f"### Thank You ###")
                st.session_state.generating = False
                st.session_state.total_no_resumes = None
                st.session_state.index = 0
                st.session_state.resumes = []  # Clear resumes when done
                st.session_state.job_description = None
            # st.session_state.user_feedback = st.text_input("should I proceed for Scheduling Interview ?")
            # st.session_state.subxmitted = st.form_submit_button("P

    def fitmentiq_generation(self):

        if st.session_state.generating:
            st.session_state.FitmentIQ = self.generate_fitmentiq()
        elif st.session_state.result:
            st.header(f"## Candidate:{st.session_state.index}")
            for res in st.session_state.previous_results: 
                with st.chat_message("AI"):
                    st.write(f"Agent Name: {res.get('Agent_Name')}")
                    st.write(res.get("output"))
                
            if st.session_state.result and not st.session_state.feedback_submitted:
                st.session_state.user_feedback = st.text_input("should I proceed for Scheduling Interview ?(Please convey in few words )", "Yes I want to schedule")
                proceed_button = st.button("Proceed")
                if proceed_button:
                    st.session_state.submitted = True
                    st.session_state.feedback_submitted = True
                    st.rerun()
            if st.session_state.submitted and st.session_state.feedback_submitted:
                # print('######## iam here ########')
                input = f"""create Prompt to Draft an email to a candidate email(Found in candidate Info) scheduling a screening interview Based on Human decision.The email should be personalized and include information about the candidate, the job description, and the decision maker(s) involved in the interview process.\nHuman decision :\n {st.session_state.user_feedback}\ncandidate Info :\n {st.session_state.result.tasks_output[0]}\nJob description :\n {st.session_state.jd_data}\n"""
                
                # input = f"{st.session_state.result.tasks_output[-1]}\nHuman Des"
                agent = GmailAgent(
                            token_file="token.json",
                            client_secrets_file="credentials.json",
                            scopes=["https://mail.google.com/"],
                            model_name="llama3-8b-8192",
                            api_base="https://api.groq.com/openai/v1",
                            api_key=os.getenv("OPENAI_API_KEY")
                        )
                agent.create_draft(input)
                next = st.button("Proceed to Next Candidate")
                if next:
                    st.session_state.previous_results.clear()
                    st.session_state.user_feedback = None
                    st.session_state.submitted = False
                    st.session_state.result = None
                    st.session_state.feedback_submitted = False
                    st.session_state.generating = True
                    st.session_state.jd_data = None
                    st.session_state.resume_data = None
                    st.rerun()
        # if st.session_state.FitmentIQ and st.session_state.FitmentIQ != "":
        #     with st.container():
        #         st.write("FitmentIQ generated successfully!")
        #         # st.download_button(
        #         #     label="Download HTML file",
        #         #     data=st.session_state.newsletter,
        #         #     file_name="newsletter.html",
        #         #     mime="text/html",
        #         # )
        #     st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("FitmentIQ Generator")

            st.write(
                """
                To generate a FitmentIQ report, upload a Job description document and a set of resumes. \n
                Your team of AI agents will generate a report of each Individual for you!
                """
            )

            job_description = st.file_uploader("Upload Job Description (PDF)", type="pdf")
            resumes = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)

            if st.button("Generate FitmentIQ"):
                if job_description is not None and resumes:
                    st.session_state.generating = True
                    st.session_state.job_description = job_description.getvalue()
                    st.session_state.resumes = [resume.getvalue() for resume in resumes]
                    st.session_state.total_no_resumes = len(resumes)
                else:
                    st.error("Please upload both a job description and at least one resume.")


    def render(self):
        st.set_page_config(page_title="FitmentIQ Generation", page_icon="📧")

        if "job_description" not in st.session_state:
            st.session_state.job_description = ""

        if "resumes" not in st.session_state:
            st.session_state.resumes = ""

        if "FitmentIQ" not in st.session_state:
            st.session_state.FitmentIQ = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False
        
        if "user_feedback" not in st.session_state:
            st.session_state.user_feedback = None

        if "submitted" not in st.session_state:
            st.session_state.submitted = False

        if "result" not in st.session_state:
            st.session_state.result = None
        
        if "index" not in st.session_state:
            st.session_state.index = 0

        if "total_no_resumes" not in st.session_state:
            st.session_state.total_no_resumes = None


        if "feedback_submitted" not in st.session_state:
            st.session_state.feedback_submitted = False

        if "jd_data" not in st.session_state:
            st.session_state.jd_data = None
        
        if "resume_data" not in st.session_state:
            st.session_state.resume_data = None

        if "previous_results" not in st.session_state:
            st.session_state.previous_results = []

        self.sidebar()

        self.fitmentiq_generation()


if __name__ == "__main__":
    FitmentiqGenUI().render()