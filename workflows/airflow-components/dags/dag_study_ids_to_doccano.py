from kaapana.operators.LocalMinioOperator import LocalMinioOperator

from kaapana.operators.LocalUnzipFileOperator import LocalUnzipFileOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator

from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from datetime import timedelta
from airflow.models import DAG

from doccano.LocalDoccanoUploadDatasetOperator import LocalDoccanoUploadDatasetOperator
from doccano.LocalCreateStudyIDJsonOperator import LocalCreateStudyIDJsonOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator

log = LoggingMixin().log

ui_forms = {
    "workflow_form": {
        "type": "object",
        "properties": {
            "name": {
                "title": "Name",
                "description": "Give your project a name for doccano.",
                "type": "string",
                "readOnly": False,
                "required": True
            },
            "description": {
                "title": "Description",
                "description": "Give some infos about your project.",
                "type": "string",
                "readOnly": False,
                "required": True
            },
            "project_type": {
                "title": "Project type",
                "default": "DocumentClassification",
                "description": "Choose a project type",
                "enum": ["DocumentClassification", "Seq2seq"],
                "type": "string",
                "readOnly": False,
                "required": True
            }
        }
    }
}

args = {
    'ui_visible': True,
    'ui_forms': ui_forms,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 0,
    'retry_delay': timedelta(seconds=60)
}

dag = DAG(
    dag_id='study-ids-to-doccano',
    default_args=args,
    schedule_interval=None)


get_input = LocalGetInputDataOperator(dag=dag, operator_out_dir='get-input-data', data_type='json')
create_doccano_json = LocalCreateStudyIDJsonOperator(dag=dag, input_operator=get_input)
doccano_upload = LocalDoccanoUploadDatasetOperator(dag=dag, input_operator=create_doccano_json)
# unzip_files = LocalUnzipFileOperator(dag=dag, input_operator=get_object_from_minio)
# upload_project = LocalNLPUploadProjectOperator(dag=dag, input_operator=unzip_files, upload_user='jipuser')
# #dicom_send = DcmSendOperator(dag=dag, input_operator=unzip_files, ae_title='uploaded')
# remove_object_from_minio = LocalMinioOperator(dag=dag, parallel_id='removing', action='remove', trigger_rule=TriggerRule.ALL_DONE)

get_input >> create_doccano_json >> doccano_upload
# get_input >> unzip_files >> upload_project >> remove_object_from_minio