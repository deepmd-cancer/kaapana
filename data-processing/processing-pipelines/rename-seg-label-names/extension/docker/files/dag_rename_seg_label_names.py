from datetime import datetime, timedelta

from kaapana.operators.LocalWorkflowCleanerOperator import LocalWorkflowCleanerOperator
from kaapana.operators.LocalGetInputDataOperator import LocalGetInputDataOperator
from kaapana.operators.LocalGetRefSeriesOperator import LocalGetRefSeriesOperator
from kaapana.operators.Mask2nifitiOperator import Mask2nifitiOperator
from rename_seg_label_names.LocalModifySegLabelNamesOperator import (
    LocalModifySegLabelNamesOperator,
)
from kaapana.operators.Itk2DcmSegOperator import Itk2DcmSegOperator
from kaapana.operators.DcmSendOperator import DcmSendOperator
from kaapana.operators.CombineMasksOperator import CombineMasksOperator
from airflow.utils.dates import days_ago
from airflow.models import DAG


ui_forms = {
    "workflow_form": {
        "type": "object",
        "properties": {
            "input": {
                "title": "Input Modality",
                "default": "SEG",
                "description": "Expected input modality.",
                "type": "string",
                "readOnly": True,
                "required": True,
            },
            "old_labels": {
                "title": "Old Labels",
                "description": "Old segmentation label names which should be overwritten; SAME ORDER AS NEW LABEL NAMES REQUIRED!!!",
                "type": "string",
                "readOnly": False,
            },
            "new_labels": {
                "title": "New Labels",
                "description": "New segmentation label names which should overwrite the old segmentation label names; SAME ORDER AS OLD LABEL NAMES REQUIRED!!!",
                "type": "string",
                "readOnly": False,
            },
            "single_execution": {
                "title": "single execution",
                "description": "Should each series be processed separately?",
                "type": "boolean",
                "default": False,
                "readOnly": False,
            },
        },
    }
}

args = {
    "ui_visible": True,
    "ui_forms": ui_forms,
    "owner": "kaapana",
    "start_date": days_ago(0),
    "retries": 0,
    "retry_delay": timedelta(seconds=30),
}

dag = DAG(
    dag_id="rename-seg-label-names",
    default_args=args,
    concurrency=10,
    max_active_runs=1,
    schedule_interval=None,
)

get_input = LocalGetInputDataOperator(
    dag=dag, name="get-input", check_modality=True, parallel_downloads=5
)

get_ref_ct_series_from_seg = LocalGetRefSeriesOperator(
    dag=dag,
    input_operator=get_input,
    search_policy="reference_uid",
    parallel_downloads=5,
    parallel_id="ct",
    modality=None,
)

dcm2nifti_seg = Mask2nifitiOperator(
    dag=dag,
    input_operator=get_input,
    dicom_operator=get_ref_ct_series_from_seg,
)

combine_masks = CombineMasksOperator(
    dag=dag,
    input_operator=dcm2nifti_seg,
)

modify_seg_label_names = LocalModifySegLabelNamesOperator(
    dag=dag,
    input_operator=combine_masks,
    metainfo_input_operator=dcm2nifti_seg,
)

nrrd2dcmSeg_multi = Itk2DcmSegOperator(
    dag=dag,
    input_operator=get_ref_ct_series_from_seg,
    segmentation_operator=combine_masks,
    input_type="multi_label_seg",
    multi_label_seg_name="rename-seg-label-names",
    multi_label_seg_info_json="seg_info.json",
    skip_empty_slices=True,
    alg_name="rename_seg_label_names",
)

dicom_send = DcmSendOperator(
    dag=dag,
    input_operator=nrrd2dcmSeg_multi,
    ae_title="rename_labels",
)

clean = LocalWorkflowCleanerOperator(dag=dag, clean_workflow_dir=False)


(
    get_input
    >> get_ref_ct_series_from_seg
    >> dcm2nifti_seg
    >> combine_masks
    >> modify_seg_label_names
    >> nrrd2dcmSeg_multi
    >> dicom_send
    >> clean
)