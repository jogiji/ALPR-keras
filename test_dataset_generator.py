import matplotlib.pyplot as plt

from config import alpr_config as config
from licence_plate_dataset_generator import LicensePlateDatasetGenerator
from pyimagesearch.io import Hdf5DatasetLoader

loader = Hdf5DatasetLoader()
images, labels = loader.load(config.TRAIN_HDF5, shuffle=True, max_items=config.BATCH_SIZE)

trainGen = LicensePlateDatasetGenerator(images, labels, config.IMAGE_WIDTH, config.IMAGE_HEIGHT,
                                        config.POOL_SIZE, config.MAX_TEXT_LEN, config.BATCH_SIZE,
                                        config.SUN397_HDF5)

inputs, outputs = next(trainGen.generator())

cols = 2
rows = len(inputs["input"]) // cols

for i, img in enumerate(inputs["input"]):
    img = img.T.reshape(config.IMAGE_HEIGHT, config.IMAGE_WIDTH)
    plt.title(inputs["labels"][i])
    plt.axis("off")
    plt.imshow(img, cmap='Greys_r')
    plt.show()

image_index = 0
f, axarr = plt.subplots(rows, cols, figsize=(15, 10))
for r in range(rows):
    for c in range(cols):
        image = inputs["input"][image_index].T.reshape(config.IMAGE_HEIGHT, config.IMAGE_WIDTH)
        axarr[r, c].axis("off")
        axarr[r, c].title.set_text(labels[image_index])
        axarr[r, c].imshow(image, cmap='gray')
        image_index += 1

plt.show()
