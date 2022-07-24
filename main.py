import os
import supervisely as sly
from dotenv import load_dotenv


load_dotenv("~/supervisely.env")
api = sly.Api.from_env()

project_id = int(os.environ["context.workspaceId"])
project = api.project.get_info_by_id(project_id)
if project is None:
    raise KeyError(f"Project with ID {project_id} not found in your account")
print(f"Project info: {project.name} (id={project.id})")

datasets = api.dataset.get_list(project.id)
print(f"There are {len(datasets)} in project")

for dataset in datasets:
    print(f"Dataset {dataset.id} has {dataset.items_count} images")
    images = api.image.get_list(dataset.id)
    for image in images:
        ann_json = api.annotation.download_json(image.id)
        ann = sly.Annotation.from_json(ann_json)
        print(f"There are {len(ann.labels)} objects on image {image.name}")
