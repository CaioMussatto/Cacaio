import joblib
import gseapy as gp

sc_samples = joblib.load('sc_samples.pkl')

degs = joblib.load('degs.pkl')

libraries = gp.get_library_name(organism="Human")
