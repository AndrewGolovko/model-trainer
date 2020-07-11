from trainer_app import create_app
from flask import abort
from trainer_app.trainer import LRPipeline, NNPipeline, TreePipeline

from rq import get_current_job
from app.models import Task
from app.rest.models.service import create_model
from app import db


app = create_app()
app.app_context().push()


def train_model(model_type: str = 'lr', **model_params) -> str:
    if model_type == "lr":
        trainer = LRPipeline(model_type)
    elif model_type == "nn":
        trainer = NNPipeline(model_type,
                            **model_params.get('nn_settings', {}))
    elif model_type == "hgbr":
        trainer = TreePipeline(model_type,
                              **model_params.get('hgbr_settings', {}))
    else:
        trainer = None
        abort(400)
    model_id = trainer.run()

    job = get_current_job()
    if job:
        task = Task.query.filter(Task.job_id == job.get_id()).first()
        task.update_task_progress()
        if (job.meta['progress'] == 100):
            create_model({"name" :model_id})
            task.model_id = model_id
            db.session.commit()

    return model_id