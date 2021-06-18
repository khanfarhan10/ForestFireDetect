virtualenv FireEnv
FireEnv\Scripts\activate
conda.bat deactivate


cd FresnelTask
pip install -r requirements.txt
pip list -> full_reqs.txt

streamlit run app.py


python assets/code/example.py
python assets/code/RastriginSol1v3.py
python assets/code/FUGChemSolv1.py - review needed by chemical engg
ipython kernel install --user --name=MonteCarlo