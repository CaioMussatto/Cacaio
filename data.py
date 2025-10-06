import joblib
import gseapy as gp

# Carrega os dados com segurança
lung_model = joblib.load("Lung_model.pkl")
lung_degs = joblib.load("DEGS_Lung.pkl")

# Define os samples disponíveis
sc_samples = {"Lung": lung_model, "Pancreas": None}

degs = {'Lung': lung_degs}
# Carrega as bibliotecas do enrichr
libraries = gp.get_library_name(organism="Human")
