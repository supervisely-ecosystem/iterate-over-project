import os
import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()

project_id = sly.env.project_id()
project = api.project.get_info_by_id(project_id)

print(f"Project info: {project.name} (id={project.id})")

# get project meta - collection of annotation classes and tags
meta_json = api.project.get_meta(project.id)
project_meta = sly.ProjectMeta.from_json(meta_json)
print(project_meta)

datasets = api.dataset.get_list(project.id)
print(f"There are {len(datasets)} datasets in project")

for dataset in datasets:
    print(f"Dataset {dataset.name} has {dataset.items_count} images")
    images = api.image.get_list(dataset.id)
    for image in images:
        ann_json = api.annotation.download_json(image.id)
        ann = sly.Annotation.from_json(ann_json, project_meta)
        print(f"There are {len(ann.labels)} objects on image {image.name}")
