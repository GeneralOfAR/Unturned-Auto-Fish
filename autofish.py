import time
import pyautogui
import soundcard as sc
import numpy as np
import warnings

# Suppress the harmless SoundcardRuntimeWarning
warnings.filterwarnings("ignore", category=sc.SoundcardRuntimeWarning)

# Audio settings
CHUNK = 1024
RATE = 44100
CHANNELS = 1
THRESHOLD = 0.030  # Adjust based on your game volume
LOOPBACK_MIC_NAME = 'CABLE Output (VB-Audio Virtual Cable)'  # Update if needed

# Mouse settings
HOLD_DURATION = 1.9

# Timing settings
INITIAL_DELAY = 15     # Ignore bobber splash
LISTEN_TIMEOUT = 30    # Max listen time before recast

print("Starting in 5 sec, pull your fishing rod out and click on unturned ")
time.sleep(5)  # Time to prepare in-game

def cast_line():
    print("Casting line...")
    pyautogui.mouseDown(button='left')
    time.sleep(HOLD_DURATION)
    pyautogui.mouseUp(button='left')

def detect_sound_with_timeout():
    loopback_mic = sc.get_microphone(LOOPBACK_MIC_NAME, include_loopback=True)
    print(f"Listening for bite sound (timeout: {LISTEN_TIMEOUT}s)...")
    
    start_time = time.time()
    
    with loopback_mic.recorder(samplerate=RATE, channels=CHANNELS, blocksize=CHUNK) as mic:
        while True:
            if time.time() - start_time > LISTEN_TIMEOUT:
                print("No bite detected within timeout. Recasting...")
                return False
            
            data = mic.record(numframes=CHUNK)
            rms = np.sqrt(np.mean(data**2))

            # Optional: uncomment for tuning THRESHOLD
            print(f"RMS: {rms:.4f}")

            if rms > THRESHOLD:
                print("Fish bite detected! Hooking...")
                return True
            
            time.sleep(0.01)

if __name__ == "__main__":
    print("Unturned Auto-Fish Script started (with timeout recast).")
    print("Press Ctrl+C to stop.")
    try:
        while True:
            cast_line()
            
            print(f"Waiting {INITIAL_DELAY}s to ignore bobber splash...")
            time.sleep(INITIAL_DELAY)
            
            fish_detected = detect_sound_with_timeout()
            
            if fish_detected:
                pyautogui.click(button='left')  # Hook
                time.sleep(1.5)  # Wait after hook
            else:
                print("Pulling in line and recasting...")
                pyautogui.click(button='right')  # Reel in
                time.sleep(1.5)
            
            if fish_detected:
                time.sleep(2)  # Extra delay only after catch

    except KeyboardInterrupt:
        print("\nScript stopped.")
