# macOS script to delete existing venv and create a new one. Make sure that the venv your are deleting is already deactivated by "deactivate"
# Some issues occured with numpy and pandas not installing from source (i.e. from directory ending in ../site-packages/)
# If permission denied, run "chmod +x debug.sh"
# After script runs, need to reactivate venv by "source venv/bin/activate"

rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --no-cache-dir