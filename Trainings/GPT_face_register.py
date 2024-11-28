import face_recognition
import cv2
import os
import pickle
import dlib

# Directory to store face data
data_dir = "face_data"
os.makedirs(data_dir, exist_ok=True)

# Path to the shape predictor model
path_to_model = r"C:\Users\User\Desktop\classes\26_11\env\Lib\site-packages\face_recognition_models\models\shape_predictor_68_face_landmarks.dat"

# Ensure the model file is loaded explicitly
try:
    face_recognition.api.pose_predictor_68_point = dlib.shape_predictor(path_to_model)
except RuntimeError as e:
    print(f"[ERROR] Unable to load model: {e}")
    exit(1)

def capture_face():
    # Start the webcam
    video_capture = cv2.VideoCapture(0)
    print("[INFO] Look at the camera to capture your face.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Could not access the camera.")
            break

        # Convert the frame to RGB (face_recognition requires RGB format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face locations
        face_locations = face_recognition.face_locations(rgb_frame)
        if len(face_locations) > 0:
            # Draw rectangles around detected faces for visual feedback
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow('Video', frame)
            print(f"[INFO] {len(face_locations)} face(s) detected. Press 'c' to capture or 'q' to quit.")
        else:
            cv2.imshow('Video', frame)
            print("[INFO] No face detected. Please adjust your position.")

        # Press 'c' to capture or 'q' to quit
        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            if len(face_locations) == 1:
                print("[INFO] Face captured.")
                video_capture.release()
                cv2.destroyAllWindows()
                return rgb_frame
            else:
                print("[ERROR] Make sure exactly one face is visible.")
        elif key & 0xFF == ord('q'):
            print("[INFO] Capture cancelled.")
            video_capture.release()
            cv2.destroyAllWindows()
            return None


def register_user():
    name = input("Enter your name: ").strip()
    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    face_file = os.path.join(data_dir, f"{name}.pkl")
    if os.path.exists(face_file):
        print("[ERROR] User already exists.")
        return

    frame = capture_face()
    if frame is None:
        return

    face_encodings = face_recognition.face_encodings(frame)
    if len(face_encodings) == 1:
        with open(face_file, "wb") as f:
            pickle.dump(face_encodings[0], f)
        print(f"[INFO] User '{name}' registered successfully.")
    else:
        print("[ERROR] Failed to register face. Make sure only one face is visible.")

def login_user():
    print("[INFO] Look at the camera to login.")
    frame = capture_face()
    if frame is None:
        return

    face_encodings = face_recognition.face_encodings(frame)
    if len(face_encodings) != 1:
        print("[ERROR] Make sure only one face is visible.")
        return

    user_face_encoding = face_encodings[0]

    # Compare against saved users
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".pkl"):
            with open(os.path.join(data_dir, file_name), "rb") as f:
                saved_face_encoding = pickle.load(f)
                match = face_recognition.compare_faces([saved_face_encoding], user_face_encoding)
                if match[0]:
                    print(f"[INFO] Login successful. Welcome, {file_name[:-4]}!")
                    return

    print("[ERROR] Face not recognized. Login failed.")

def main():
    while True:
        print("\n1. Register User")
        print("2. Login User")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
