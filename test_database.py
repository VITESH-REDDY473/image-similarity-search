from database_manager import get_all_images

images = get_all_images()

print("Total Images:", len(images))

for image in images:
    print(image["image_name"])