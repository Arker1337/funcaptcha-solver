from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="images")
types = ['butterfly', 'camel']
trainer.setTrainConfig(object_names_array=types, batch_size=4, num_experiments=1)
trainer.trainModel()
