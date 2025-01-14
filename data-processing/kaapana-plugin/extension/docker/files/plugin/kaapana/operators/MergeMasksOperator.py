from datetime import timedelta

from kaapana.operators.KaapanaBaseOperator import KaapanaBaseOperator
from kaapana.blueprints.kaapana_global_variables import (
    DEFAULT_REGISTRY,
    KAAPANA_BUILD_VERSION,
)


class MergeMasksOperator(KaapanaBaseOperator):
    """
    MergeMasksOperator

    Searches for NIFTI files (expects segmentation masks) in operator input-dir and merges them according to the given mode.
    mode can either be "combine" (default) or "fuse".

    mode = "combine": combines NIFTI files into a single NIFTI-file; labels that overlap with already combined labels are sorted out.
    mode = "fuse": fuses label masks of specified labels (via label_name) into a single NIFTI file.

    **Inputs:**
    * mode: either "combine" or "fuse"
    * fuse_label_names: label_names of segmentation masks which should be fused
    * fused_label_name: new label name of fused segmentation masks
    * input Nifti files

    **Outputs:**
    * Nifti file(s) with merged (combined or fused) segmentation masks
    * adapted seg_info and meta_info JSON files

    """

    execution_timeout = timedelta(minutes=60)

    def __init__(
        self,
        dag,
        name="combine-masks",
        mode="combine",
        env_vars=None,
        execution_timeout=execution_timeout,
        **kwargs,
    ):
        ram_mem_mb = 8000
        gpu_mem_mb = None

        if env_vars is None:
            env_vars = {}
        envs = {
            "MODE": str(mode),
        }
        env_vars.update(envs)

        super().__init__(
            dag=dag,
            image=f"{DEFAULT_REGISTRY}/merge-masks:{KAAPANA_BUILD_VERSION}",
            name=name,
            image_pull_secrets=["registry-secret"],
            execution_timeout=execution_timeout,
            keep_parallel_id=False,
            enable_proxy=True,
            env_vars=env_vars,
            ram_mem_mb=ram_mem_mb,
            gpu_mem_mb=gpu_mem_mb,
            **kwargs,
        )
