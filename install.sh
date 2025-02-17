git clone https://github.com/cltl/DFNDataReleases.git
cd DFNDataReleases
pip install -r requirements.txt
bash install.sh
rm -r unstructured
rm -r structured
cp -r ../structured .
cp -r ../unstructured .
