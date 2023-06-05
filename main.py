import cv2
import numpy as np

def measure_diameter(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection to detect edges
    edges = cv2.Canny(blurred, 50, 150)
    
    # Perform Hough line transformation to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    
    # Calculate the diameters
    if lines is not None:
        inner_diameters = []
        outer_diameters = []
        
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            
            # Calculate the distance between the two points
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            
            # Assuming the longer lines are the outer diameter
            if distance > 50:
                outer_diameters.append(distance)
            else:
                inner_diameters.append(distance)
        
        # Calculate the average diameter
        if inner_diameters:
            avg_inner_diameter = sum(inner_diameters) / len(inner_diameters)
            print("Inner diameter:", avg_inner_diameter)
        else:
            print("No inner diameter detected.")
        
        if outer_diameters:
            avg_outer_diameter = sum(outer_diameters) / len(outer_diameters)
            print("Outer diameter:", avg_outer_diameter)
        else:
            print("No outer diameter detected.")
    else:
        print("No lines detected.")

# Call the function for each image
image_paths = ["needle_image1.jpg", "needle_image2.jpg", "needle_image3.jpg"]
for path in image_paths:
    print("Image:", path)
    measure_diameter(path)
    print()
