import os
import torch

import detectron2.data.transforms as T
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.data import MetadataCatalog
from detectron2.modeling import build_model


class DoublePredictor:

	def __init__(self, cfg, cfg2):
		self.cfg = cfg.clone()  # cfg can be modified by model
		self.cfg2 = cfg2.clone()
		self.model = build_model(self.cfg)
		self.model2 = build_model(self.cfg2)
		self.model.eval()
		self.model2.eval()
		if len(cfg.DATASETS.TEST):
			self.metadata = MetadataCatalog.get(cfg.DATASETS.TEST[0])
		checkpointer = DetectionCheckpointer(self.model)
		checkpointer2 = DetectionCheckpointer(self.model2)
		checkpointer.load(cfg.MODEL.WEIGHTS)
		checkpointer2.load(cfg2.MODEL.WEIGHTS)

		self.aug = T.ResizeShortestEdge([cfg.INPUT.MIN_SIZE_TEST, cfg.INPUT.MIN_SIZE_TEST], cfg.INPUT.MAX_SIZE_TEST)
		self.aug2 = T.ResizeShortestEdge([cfg2.INPUT.MIN_SIZE_TEST, cfg2.INPUT.MIN_SIZE_TEST], cfg.INPUT.MAX_SIZE_TEST)

		self.input_format = cfg.INPUT.FORMAT
		assert self.input_format in ["RGB", "BGR"], self.input_format

	def __call__(self, original_image):
		with torch.no_grad():
			# Apply pre-processing to image.
			if self.input_format == "RGB":  # whether the model expects BGR inputs or RGB
				original_image = original_image[:, :, ::-1]
			height, width = original_image.shape[:2]
			image = self.aug.get_transform(original_image).apply_image(original_image)
			image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))

			inputs = {"image": image, "height": height, "width": width}
			predictions = self.model([inputs])[0]
			predictions2 = self.model2([inputs])[0]
			return predictions, predictions2
