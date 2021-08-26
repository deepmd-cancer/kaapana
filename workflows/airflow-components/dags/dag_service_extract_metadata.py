from kaapana.operators.LocalDcm2JsonOperator import LocalDcm2JsonOperator
from kaapana.operators.LocalJson2MetaOperator import LocalJson2MetaOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import DAG
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator

log = LoggingMixin().log

args = {
    'ui_visible': False,
    'owner': 'kaapana',
    'start_date': days_ago(0),
    'retries': 2,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    dag_id='service-extract-metadata',
    default_args=args,
    concurrency=50,
    max_active_runs=20,
    schedule_interval=None
)

get_input = LocalGetInputDataOperator(dag=dag, operator_out_dir='get-input-data')
extract_metadata = LocalDcm2JsonOperator(dag=dag, input_operator=get_input, delete_private_tags=True)
push_json = LocalJson2MetaOperator(dag=dag, input_operator=get_input, json_operator=extract_metadata)
clean = LocalWorkflowCleanerOperator(dag=dag, clean_workflow_dir=True)

get_input >> extract_metadata >> push_json >> clean
