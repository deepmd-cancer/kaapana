FROM local-only/base-python-cpu:latest

LABEL IMAGE="dicom-init"
LABEL VERSION="0.1.3"
LABEL BUILD_IGNORE="False"

WORKDIR /kaapana/app

RUN curl --output /test-dicoms.zip "https://www.kaapana.ai/kaapana-downloads/kaapana-build-files/init-dicoms/0.0.4/init-dicoms.zip" \
    && mkdir -p /dicom_test_data && unzip /test-dicoms.zip -d /dicom_test_data && rm -rf test-dicoms.zip

COPY files/requirements.txt /kaapana/app/
RUN python3 -m pip install -c https://raw.githubusercontent.com/kaapana/kaapana/0.2.1/build-scripts/constraints-0.2.1.txt --no-cache-dir -r /kaapana/app/requirements.txt && rm /kaapana/app/requirements.txt 

COPY files/start.py /kaapana/app/start.py
COPY files/HelperDcmWeb.py /kaapana/app/HelperDcmWeb.py

CMD ["python3","-u","/kaapana/app/start.py"]