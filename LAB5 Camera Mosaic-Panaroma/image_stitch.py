import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load images from paths and convert to RGB
def load_images(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Warning: Unable to load image at path {path}")
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)
    return images

# Detect keypoints and compute descriptors using Harris corners and ORB
def detect_and_compute_keypoints(image, harris_threshold=0.01, orb_features=1000):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = np.float32(gray)
    harris_corners = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
    harris_corners = cv2.dilate(harris_corners, None)

    # Extract strong corners above threshold
    keypoints = np.argwhere(harris_corners > harris_threshold * harris_corners.max())
    keypoints = [cv2.KeyPoint(float(x[1]), float(x[0]), 1) for x in keypoints]

    # Compute descriptors for detected keypoints with ORB
    orb = cv2.ORB_create(nfeatures=orb_features)
    keypoints, descriptors = orb.compute(image, keypoints)
    return keypoints, descriptors

# Stitch images using detected keypoints and RANSAC homography estimation
def stitch_images(images, ransac_thresh=5.0):
    stitched_image = images[0]  # Initialize with the first image

    for i in range(1, len(images)):
        keypoints1, descriptors1 = detect_and_compute_keypoints(stitched_image)
        keypoints2, descriptors2 = detect_and_compute_keypoints(images[i])

        # Match features using Hamming distance
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)

        # Extract coordinates of matched points
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Find homography with RANSAC to align images
        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, ransac_thresh)
        
        # Compute size of the resulting stitched image canvas
        height, width, _ = stitched_image.shape
        warped_image = cv2.warpPerspective(images[i], H, (width + images[i].shape[1], height))

        # Overlay stitched image to form the panorama
        warped_image[0:height, 0:width] = stitched_image
        stitched_image = crop_black_borders(warped_image)  # Crop out excess borders

    return stitched_image

# Crop black borders from the stitched panorama for a cleaner look
def crop_black_borders(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        return image[y:y+h, x:x+w]
    return image

# Main function to stitch images and visualize the result
def main():
  
    image_paths = [
    "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data\\image_1-1.jpg",
    "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data\\image_2-1.jpg",
    "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data\\image_3-1.jpg",
    "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data\\image_4-1.jpg",
    "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data\\image_5-1.jpg",
    "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data\\image_6-1.jpg"
]

    images = load_images(image_paths)

    # Check if images loaded successfully
    if not images:
        print("No images loaded. Please check the file paths.")
        return

    # Stitch images with adjustable RANSAC threshold
    ransac_threshold = 5.0  # Adjust this based on image overlap (higher for less overlap)
    stitched_image = stitch_images(images, ransac_thresh=ransac_threshold)

    # Display the final stitched image
    plt.figure(figsize=(10, 5))
    plt.imshow(stitched_image)
    plt.axis('off')
    plt.show()

# Execute the main function
if __name__ == "__main__":
    main()
