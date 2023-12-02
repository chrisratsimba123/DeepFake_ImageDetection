import tensorflow as tf
import os
import numpy as np

execution_path = os.getcwd()


def predict_img(filename):
    # print('Filname is ' + filename)
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    # target = filename  # location of image present in temp directory
    image_height = 256
    image_width = 256
    model_path = os.path.join(os.getcwd(), "model")
    print('model path' + model_path)

    loaded_model = tf.saved_model.load(export_dir=os.path.join(execution_path, "model/base_model"),
                                       tags=['serve'])
    class_names = ['fake', 'real']

    img = tf.keras.utils.load_img(
        filename, target_size=(image_height, image_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = loaded_model(img_array)
    score = tf.nn.softmax(predictions[0])
    d = [class_names[np.argmax(score)], round(100 * np.max(score), 2)]
    # os.remove(target)  # delete temporary file

    return d
