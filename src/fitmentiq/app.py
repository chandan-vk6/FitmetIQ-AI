import streamlit as st
from crew import FitmentiqCrew
import tempfile
import os

class FitmentiqGenUI:

    # def load_html_template(self):
    #     with open("src/newsletter_gen/config/newsletter_template.html", "r") as file:
    #         html_template = file.read()

    #     return html_template

    def generate_fitmentiq(self, job_description, resumes):

        with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to temporary directory
            jd_path = os.path.join(temp_dir, "job_description.pdf")
            with open(jd_path, "wb") as f:
                f.write(job_description.getbuffer())
            
            resume_paths = []
            for i, resume in enumerate(resumes):
                resume_path = os.path.join(temp_dir, f"resume_{i}.pdf")
                with open(resume_path, "wb") as f:
                    f.write(resume.getbuffer())
                resume_paths.append(resume_path)

            dataset = [{"job_description": jd_path, "resumes": resume_path} for resume_path in resume_paths]

            return FitmentiqCrew().crew().kickoff_for_each(inputs=dataset)

    def fitmentiq_generation(self):

        if st.session_state.generating:
            st.session_state.FitmentIQ = self.generate_fitmentiq(
                st.session_state.job_description, st.session_state.resumes
            )
        # else:
        #     for res in st.session_state.previous_results:
        #         with st.chat_message("AI"):
        #             st.write(res)
        if st.session_state.FitmentIQ and st.session_state.FitmentIQ != "":
            with st.container():
                st.write("FitmentIQ generated successfully!")
                # st.download_button(
                #     label="Download HTML file",
                #     data=st.session_state.newsletter,
                #     file_name="newsletter.html",
                #     mime="text/html",
                # )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("FitmentIQ Generator")

            st.write(
                """
                To generate a FitmentIQ report, upload a Job description document and a set of resumes. \n
                Your team of AI agents will generate a report of each Individual for you!
                """
            )

            st.session_state.job_description = st.file_uploader("Upload Job Description (PDF)", type="pdf")
            st.session_state.resumes = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)

            if st.button("Generate FitmentIQ"):
                st.session_state.generating = True

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

        if "previous_results" not in st.session_state:
            st.session_state.previous_results = []

        self.sidebar()

        self.fitmentiq_generation()


if __name__ == "__main__":
    FitmentiqGenUI().render()