from kaapana.operators.LocalMinioOperator import LocalMinioOperator

from kaapana.operators.LocalUnzipFileOperator import LocalUnzipFileOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator

from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from doccano.LocalDoccanoDownloadDatasetOperator import LocalDoccanoDownloadDatasetOperator

log = LoggingMixin().log

args = {
    'ui_visible': False,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 2,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    dag_id='service-parse-doccano-tokens',
    default_args=args,
    schedule_interval=None,
    concurrency=10,
    max_active_runs=5
    )

download_dataset = LocalDoccanoDownloadDatasetOperator(dag=dag)
# get_object_from_minio = LocalMinioOperator(dag=dag, action_operator_dirs=['dicoms'], operator_out_dir='dicoms')
unzip_files = LocalUnzipFileOperator(dag=dag, input_operator=download_dataset)
# dicom_send = DcmSendOperator(dag=dag, input_operator=unzip_files, ae_title='uploaded', level='batch')
# remove_object_from_minio = LocalMinioOperator(dag=dag, parallel_id='removing', action='remove', trigger_rule=TriggerRule.ALL_DONE)
# clean = LocalWorkflowCleanerOperator(dag=dag,clean_workflow_dir=True)
download_dataset >> unzip_files
# get_object_from_minio >> unzip_files >> dicom_send >> remove_object_from_minio >> clean
