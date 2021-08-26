import os
import glob
from datetime import timedelta
import pydicom

from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator, default_registry, default_project
from kaapana.blueprints.kaapana_global_variables import BATCH_NAME, WORKFLOW_DIR


class DcmSendOperator(KaapanaBaseOperator):

    def __init__(self,
                 dag,
                 ae_title='NONE',
                 pacs_host='ctp-dicom-service.flow.svc',
                 pacs_port='11112',
                 env_vars=None,
                 level='element',
                 check_arrival=False,
                 enable_proxy=False,
                 host_network=False,
                 execution_timeout=timedelta(minutes=20),
                 *args, **kwargs
                 ):

        if level not in ['element', 'batch']:
            raise NameError('level must be either "element" or "batch". \
                If batch, an operator folder next to the batch folder with .dcm files is expected. \
                If element, *.dcm are expected in the corresponding operator with .dcm files is expected.'
                            )

        if env_vars is None:
            env_vars = {}

        envs = {
            "HOST": str(pacs_host),
            "PORT": str(pacs_port),
            "AETITLE": str(ae_title),
            "CHECK_ARRIVAL": str(check_arrival),
            "LEVEL": str(level)
        }

        env_vars.update(envs)

        super().__init__(
            dag=dag,
            image=f"{default_registry}/dcmsend:3.6.4-vdev",
            name="dcmsend",
            image_pull_secrets=["registry-secret"],
            env_vars=env_vars,
            host_network=host_network,
            enable_proxy=enable_proxy,
            execution_timeout=execution_timeout,
            *args, **kwargs
        )
