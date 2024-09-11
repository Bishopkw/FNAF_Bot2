from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Prepare data generators (assuming multiple classes are organized in subdirectories)
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_generator = train_datagen.flow_from_directory(
    'data/freddy/sorted/',
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',  # Switch to 'categorical' for multi-class
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'data/freddy/sorted/',
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',  # Switch to 'categorical' for multi-class
    subset='validation'
)

# Build a CNN model for multi-class classification
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(3, activation='softmax')  # 'num_classes' should be the number of classes
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_generator, epochs=20, validation_data=validation_generator)

# Save the model
model.save('freddy_detector.h5')
