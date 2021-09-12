echo 'Downloading data from Zenodo'
echo '============================'
python download_data.py

echo ''
echo 'Building Docker container'
echo '========================='
docker build -t relm_rp .

echo ''
echo 'Running experiment'
echo '=================='
echo ''
docker run -t -i -v $PWD/output:/app/output relm_rp

