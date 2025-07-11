import streamlit as st

st.set_page_config(page_title="LCA Dashboard", layout="wide")

# --- Combined Thesis Header, Dashboard Purpose, Structure, Contact ---
st.markdown("""
# 🎓 Interactive Supplementary Dashboard  
#### *Prospective LCA of Sustainable Aviation Fuels*  
##### *Scenario-Based Assessment Using Integrated Assessment Models (2020–2050)*

This dashboard serves as a supplementary component to the Master's thesis submitted in partial fulfillment of the requirements for the degree **Master of Science (M.Sc.)**  
at the **TUM School of Life Sciences**, Technical University of Munich.

The thesis explores the prospective environmental performance of various Sustainable Aviation Fuel (SAF) production pathways.  
It applies a harmonized Life Cycle Assessment (LCA) approach based on the ISO 14040/44 framework,  
integrating forward-looking scenarios from Integrated Assessment Models (IAMs) over the period 2020 to 2050.

All interactive modules in this dashboard aim to ensure transparent, reproducible, and accessible dissemination of LCA findings.

---

## 📂 Structure and Content

**(1) Overview**  
Provides a comparative summary of environmental impacts across SAF pathways, including GHG and non-GHG indicators.

**(2) Monetization**  
Displays the external costs associated with each pathway by converting midpoint environmental impacts into economic terms (€/kg fuel), based on EF 3.1 monetization factors.

**(3) Process Contribution**  
Breaks down the relative contribution of individual unit processes (e.g., feedstock supply, synthesis) to the overall impact profile of each fuel.

**(4) Process Heatmap**  
Visualizes process-specific environmental burdens across multiple impact categories to identify environmental hotspots.

**(5) Prospective**  
Presents forward-looking emission trends under three IAM-based scenarios (Optimistic, Middle, Pessimistic) from 2020 to 2050.

**(6) Raw Data**  
Provides access to selected life cycle inventory (LCI) results and characterization scores used in the thesis, for transparency and potential reuse.

---

## 📫 Contact

**Advisor**  
Univ.-Prof. Dr.-Ing. Agnes Jocher  
*Assistant Professorship of Sustainable Future Mobility*  

**Submitted by**  
Mingyu Song  

**Submission Date**  
08.01.2025, München

For academic or professional inquiries regarding this work, please contact:  
**Mingyu Song**  
Master's Student, Sustainable Resource Management  
Technical University of Munich  
📧 mingyu.song@tum.de  
🔗 [LinkedIn](https://www.linkedin.com/in/your-profile/) *(optional)*

---

### 🙏 Acknowledgement

Special thanks to **Univ.-Prof. Dr.-Ing. Agnes Jocher** for her invaluable guidance, support, and academic mentorship throughout the development of this thesis and accompanying dashboard.
""", unsafe_allow_html=True)
