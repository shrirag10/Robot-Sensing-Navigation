import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load and resize images to 1000x1000
def load_and_resize_images(image_paths, size=(1000, 1000)):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Warning: Unable to load image at path {path}")
            continue
        img = cv2.resize(img, size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)
    return images

# Detect Harris corners and add dense grid-based keypoints
def detect_harris_and_grid_keypoints(image, harris_threshold=0.001, grid_spacing=30):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Harris corner detection
    gray_float = np.float32(gray)
    harris_corners = cv2.cornerHarris(gray_float, blockSize=2, ksize=3, k=0.04)
    harris_corners = cv2.dilate(harris_corners, None)

    # Extract points above threshold
    keypoints = np.argwhere(harris_corners > harris_threshold * harris_corners.max())
    keypoints = [cv2.KeyPoint(float(x[1]), float(x[0]), 1) for x in keypoints]

    # Add dense grid-based keypoints for better coverage
    h, w = gray.shape
    for y in range(0, h, grid_spacing):
        for x in range(0, w, grid_spacing):
            keypoints.append(cv2.KeyPoint(float(x), float(y), 1))

    # Generate descriptors
    orb = cv2.ORB_create(edgeThreshold=5, patchSize=15)
    keypoints, descriptors = orb.compute(image, keypoints)
    return keypoints, descriptors

# Stitch images with constrained homography estimation
def stitch_images(images, ransac_thresh=4.0, match_limit=50):
    stitched_image = images[0]  # Start with the first image

    for i in range(1, len(images)):
        keypoints1, descriptors1 = detect_harris_and_grid_keypoints(stitched_image)
        keypoints2, descriptors2 = detect_harris_and_grid_keypoints(images[i])

        # Match features and retain only the best matches
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)[:match_limit]

        if len(matches) < 4:
            print(f"Skipping image {i + 1} due to insufficient matches ({len(matches)} found).")
            continue

        # Extract matched points
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Calculate homography with RANSAC
        H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, ransac_thresh)
        if H is None:
            print(f"Skipping image {i + 1} due to invalid homography.")
            continue

        # Warp image and check dimensions to prevent black regions
        height, width, _ = stitched_image.shape
        warped_image = cv2.warpPerspective(images[i], H, (width + images[i].shape[1], height))
        
        # Blend images without complex masking
        stitched_image = simple_blend(stitched_image, warped_image)

    return crop_black_borders(stitched_image)

# Simple blending function to ensure overlay without complex masking
def simple_blend(base_image, new_image):
    # Ensure new_image aligns with base_image dimensions
    if new_image.shape[1] > base_image.shape[1]:
        padding = ((0, 0), (0, new_image.shape[1] - base_image.shape[1]), (0, 0))
        base_image = np.pad(base_image, padding, mode='constant', constant_values=0)
    new_image = new_image[:, :base_image.shape[1]]
    
    # Simple blend by averaging overlapping areas
    blended = np.where(new_image > 0, (base_image + new_image) // 2, base_image)
    return blended.astype(np.uint8)

# Crop black borders from the final stitched image
def crop_black_borders(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        return image[y:y+h, x:x+w]
    return image

# Main function to execute the stitching
def main():
    image_paths = [
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_1.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_2.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_3.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_4.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_5.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_6.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_7.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_9.jpg",
        "C:\\Users\\ragsh\\Desktop\\FALL 24\\RSN\\LAB5\\data-1\\image_8.jpg"
    ]

    images = load_and_resize_images(image_paths)

    if not images:
        print("No images loaded. Please check the file paths.")
        return

    # Perform stitching with constrained homography
    stitched_image = stitch_images(images, ransac_thresh=4.0)

    # Display the stitched result
    plt.figure(figsize=(10, 5))
    plt.imshow(stitched_image)
    plt.axis('off')
    plt.show()

# Execute main function
if __name__ == "__main__":
    main()
