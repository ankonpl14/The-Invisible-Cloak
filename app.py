import cv2
import numpy as np
import time

# 1. Setup Camera
cap = cv2.VideoCapture(0)

# Camera warm-up
time.sleep(3)

# 2. Capture Background
background = 0
for i in range(30):
    ret, background = cap.read()

background = cv2.flip(background, 1)
print("Background captured! Hold up your RED cloak.")

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    # Flip frame
    img = cv2.flip(img, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. RED color range (two ranges)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    # 4. Clean the mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # 5. Generate final output
    cloak_area = cv2.bitwise_and(background, background, mask=mask)
    mask_inv = cv2.bitwise_not(mask)
    current_frame = cv2.bitwise_and(img, img, mask=mask_inv)

    final_output = cv2.addWeighted(cloak_area, 1, current_frame, 1, 0)

    cv2.imshow("Harry Potter Red Cloak", final_output)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
