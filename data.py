import joblib
import gseapy as gp

lung_model = joblib.load("Lung_model.pkl")
lung_degs = joblib.load("DEGS_Lung.pkl")

sc_samples = {"Lung": lung_model, "Pancreas": None}

degs = {'Lung': lung_degs}

libraries = gp.get_library_name(organism="Human")
